"""Two-phase transfer learning for offline tomato disease detection."""

from __future__ import annotations

import json
import os
import random

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras import layers, mixed_precision, models, regularizers

import config
from data_utils import (
    compute_balanced_class_weights,
    list_image_records,
    load_square_images,
    prepare_dataset,
    save_model_metadata,
)
from leaf_gate import build_and_save_leaf_gate

TRAIN_SOURCE_SIZE = 256


def set_global_seed(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.keras.utils.set_random_seed(seed)


def configure_runtime() -> None:
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    gpus = tf.config.list_physical_devices("GPU")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    # Mixed precision helps GPUs. Keep float32 on CPU for numerical accuracy.
    if gpus:
        mixed_precision.set_global_policy("mixed_float16")
    else:
        mixed_precision.set_global_policy("float32")


def build_augmenter() -> tf.keras.Sequential:
    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.08, fill_mode="reflect"),
            layers.RandomTranslation(0.08, 0.08, fill_mode="reflect"),
            layers.RandomZoom(0.12, fill_mode="reflect"),
            layers.RandomContrast(0.15),
            layers.RandomBrightness(0.12, value_range=(0.0, 255.0)),
        ],
        name="train_augmentation",
    )


def mixup(images: tf.Tensor, labels: tf.Tensor, alpha: float = config.MIXUP_ALPHA):
    batch_size = tf.shape(images)[0]
    gamma_1 = tf.random.gamma(shape=[batch_size], alpha=alpha)
    gamma_2 = tf.random.gamma(shape=[batch_size], alpha=alpha)
    lam = gamma_1 / (gamma_1 + gamma_2)
    indices = tf.random.shuffle(tf.range(batch_size))
    lam_images = tf.reshape(lam, [batch_size, 1, 1, 1])
    lam_labels = tf.reshape(lam, [batch_size, 1])
    mixed_images = images * lam_images + tf.gather(images, indices) * (1.0 - lam_images)
    mixed_labels = labels * lam_labels + tf.gather(labels, indices) * (1.0 - lam_labels)
    return mixed_images, mixed_labels


def make_dataset(
    images: np.ndarray,
    labels: list[int],
    training: bool,
    augmenter: tf.keras.Sequential | None = None,
) -> tf.data.Dataset:
    one_hot = tf.one_hot(labels, depth=len(config.CLASS_NAMES), dtype=tf.float32)
    ds = tf.data.Dataset.from_tensor_slices((images, one_hot))
    if training:
        assert augmenter is not None
        ds = ds.shuffle(max(len(labels) * 4, 64), seed=config.SEED, reshuffle_each_iteration=True)

        def _augment(image, label):
            image = tf.image.random_crop(image, [config.IMG_SIZE, config.IMG_SIZE, 3])
            image = augmenter(image, training=True)
            return image, label

        ds = ds.map(_augment, num_parallel_calls=tf.data.AUTOTUNE)
        ds = ds.repeat()
        ds = ds.batch(config.BATCH_SIZE, drop_remainder=True)
        if config.MIXUP_ALPHA > 0:
            ds = ds.map(mixup, num_parallel_calls=tf.data.AUTOTUNE)
    else:
        ds = ds.batch(config.BATCH_SIZE)
    return ds.prefetch(tf.data.AUTOTUNE)


def build_model(num_classes: int) -> tuple[tf.keras.Model, tf.keras.Model]:
    base_model = tf.keras.applications.EfficientNetV2B0(
        include_top=False,
        weights="imagenet",
        input_shape=(config.IMG_SIZE, config.IMG_SIZE, 3),
        include_preprocessing=True,
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(config.IMG_SIZE, config.IMG_SIZE, 3), name="leaf_image")
    # EfficientNetV2 preprocessing expects [0, 255]. Keep BatchNorm in inference
    # mode so moving statistics from ImageNet stay stable during fine-tuning.
    features = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="avg_pool")(features)
    x = layers.Dropout(config.DROPOUT, name="head_dropout")(x)
    outputs = layers.Dense(
        num_classes,
        activation="softmax",
        kernel_regularizer=regularizers.l2(config.WEIGHT_DECAY),
        dtype="float32",
        name="disease_prob",
    )(x)
    model = models.Model(inputs, outputs, name="hortivision_ng")
    return model, base_model


def compile_model(model: tf.keras.Model, learning_rate: float) -> None:
    optimizer = tf.keras.optimizers.AdamW(
        learning_rate=learning_rate,
        weight_decay=config.WEIGHT_DECAY,
        clipnorm=1.0,
    )
    model.compile(
        optimizer=optimizer,
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=config.LABEL_SMOOTHING),
        metrics=[
            tf.keras.metrics.CategoricalAccuracy(name="accuracy"),
            tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top3_accuracy"),
        ],
    )


def make_callbacks(checkpoint_path: str) -> list[tf.keras.callbacks.Callback]:
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    return [
        tf.keras.callbacks.ModelCheckpoint(
            checkpoint_path,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            mode="max",
            patience=8,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
        tf.keras.callbacks.TerminateOnNaN(),
    ]


def unfreeze_for_finetuning(base_model: tf.keras.Model) -> int:
    fine_tune_at = int(len(base_model.layers) * (1.0 - config.FINE_TUNE_LAYER_FRACTION))
    base_model.trainable = True
    for idx, layer in enumerate(base_model.layers):
        freeze = idx < fine_tune_at or isinstance(layer, layers.BatchNormalization)
        layer.trainable = not freeze
    trainable = sum(int(layer.trainable) for layer in base_model.layers)
    return trainable


def evaluate_model(model: tf.keras.Model, images: np.ndarray, labels: list[int]) -> dict:
    probabilities = model.predict(images, batch_size=config.BATCH_SIZE, verbose=0)
    y_pred = np.argmax(probabilities, axis=1)
    y_true = np.array(labels)
    report = classification_report(
        y_true,
        y_pred,
        target_names=config.CLASS_NAMES,
        digits=4,
        zero_division=0,
    )
    matrix = confusion_matrix(y_true, y_pred)
    accuracy = float(np.mean(y_true == y_pred))
    print("\nValidation classification report\n")
    print(report)
    print("Confusion matrix")
    print(matrix)
    return {
        "val_accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
    }


def export_tflite(model: tf.keras.Model, tflite_path: str) -> None:
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = []
    try:
        tflite_model = converter.convert()
    except Exception:
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS,
            tf.lite.OpsSet.SELECT_TF_OPS,
        ]
        tflite_model = converter.convert()
    with open(tflite_path, "wb") as handle:
        handle.write(tflite_model)


def main() -> None:
    set_global_seed(config.SEED)
    configure_runtime()
    os.makedirs(config.MODEL_DIR, exist_ok=True)

    print("Preparing aligned RGB JPEG dataset...")
    counts = prepare_dataset()
    for key, value in counts.items():
        print(f"  {key}: {value} images")

    train_paths, train_labels = list_image_records(config.READY_TRAIN_DIR)
    val_paths, val_labels = list_image_records(config.READY_VAL_DIR)
    train_images = load_square_images(train_paths, TRAIN_SOURCE_SIZE)
    val_images = load_square_images(val_paths, config.IMG_SIZE)
    print(f"Train images: {len(train_paths)} | Validation images: {len(val_paths)}")
    print(f"Classes ({len(config.CLASS_NAMES)}): {config.CLASS_NAMES}")

    augmenter = build_augmenter()
    train_ds = make_dataset(train_images, train_labels, training=True, augmenter=augmenter)
    val_ds = make_dataset(val_images, val_labels, training=False)
    class_weight = compute_balanced_class_weights(train_labels)
    steps_per_epoch = max(config.AUGMENTED_VIEWS_PER_EPOCH // config.BATCH_SIZE, 1)
    checkpoint_path = os.path.join(config.MODEL_DIR, config.KERAS_MODEL_NAME)

    model, base_model = build_model(len(config.CLASS_NAMES))
    phase1_path = os.path.join(config.MODEL_DIR, "hortivision_phase1.keras")
    phase2_path = os.path.join(config.MODEL_DIR, "hortivision_phase2.keras")

    print("\nPhase 1: training classification head with frozen backbone...")
    compile_model(model, config.PHASE1_LR)
    history_1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=config.PHASE1_EPOCHS,
        steps_per_epoch=steps_per_epoch,
        class_weight=class_weight,
        callbacks=make_callbacks(phase1_path),
        shuffle=False,
        verbose=1,
    )

    print("\nPhase 2: fine-tuning upper EfficientNetV2 blocks...")
    if os.path.exists(phase1_path):
        model = tf.keras.models.load_model(phase1_path)
        base_model = next(layer for layer in model.layers if isinstance(layer, tf.keras.Model))
    trainable_layers = unfreeze_for_finetuning(base_model)
    print(f"Trainable backbone layers: {trainable_layers}/{len(base_model.layers)}")
    compile_model(model, config.PHASE2_LR)
    history_2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=config.PHASE2_EPOCHS,
        steps_per_epoch=steps_per_epoch,
        class_weight=class_weight,
        callbacks=make_callbacks(phase2_path),
        shuffle=False,
        verbose=1,
    )

    candidate_paths = [path for path in (phase1_path, phase2_path) if os.path.exists(path)]
    if not candidate_paths:
        candidate_paths = [checkpoint_path]
        model.save(checkpoint_path)

    best_path = candidate_paths[0]
    best_acc = -1.0
    best_model = None
    best_metrics = None
    for path in candidate_paths:
        candidate = tf.keras.models.load_model(path)
        metrics = evaluate_model(candidate, val_images, val_labels)
        print(f"{path} validation accuracy: {metrics['val_accuracy']:.4f}")
        if metrics["val_accuracy"] > best_acc:
            best_acc = metrics["val_accuracy"]
            best_path = path
            best_model = candidate
            best_metrics = metrics

    model = best_model
    metrics = best_metrics
    print(f"Selected checkpoint: {best_path} ({best_acc:.4f})")
    model.save(checkpoint_path)
    history = {
        "phase1": {key: [float(v) for v in values] for key, values in history_1.history.items()},
        "phase2": {key: [float(v) for v in values] for key, values in history_2.history.items()},
        "selected_checkpoint": best_path,
        "val_accuracy": metrics["val_accuracy"],
        "classification_report": metrics["classification_report"],
        "confusion_matrix": metrics["confusion_matrix"],
    }
    with open(os.path.join(config.MODEL_DIR, config.HISTORY_NAME), "w", encoding="utf-8") as handle:
        json.dump(history, handle, indent=2)

    tflite_path = os.path.join(config.MODEL_DIR, config.TFLITE_MODEL_NAME)
    print("Exporting full-precision TFLite model...")
    export_tflite(model, tflite_path)
    print("Building tomato-leaf rejection gate...")
    leaf_gate = build_and_save_leaf_gate(model, train_paths + val_paths)
    save_model_metadata(
        {
            "val_accuracy": metrics["val_accuracy"],
            "train_images": len(train_paths),
            "val_images": len(val_paths),
            "leaf_similarity_threshold": leaf_gate["similarity_threshold"],
            "leaf_foliage_min": leaf_gate["foliage_min"],
        }
    )
    print(f"Keras model: {checkpoint_path}")
    print(f"TFLite model: {tflite_path}")
    print(f"Leaf embed: {leaf_gate['embed_path']}")
    print(f"Validation accuracy: {metrics['val_accuracy']:.4f}")


if __name__ == "__main__":
    main()
