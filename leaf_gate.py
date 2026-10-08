"""Reject photos that are not tomato leaflets before disease classification.

The disease head always returns one of 11 classes, so fruit, people, and
other objects would otherwise be labelled as a tomato disease. This gate
uses the center square crop only (so a leafy corner cannot sneak a fruit
photo through), rejects round fruit blobs, and compares embeddings to a
leaflet-only gallery — not to fruit photos that were misfiled in train.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

import config
from image_prep import square_crop_resize, to_rgb


@dataclass(frozen=True)
class LeafGateResult:
    accepted: bool
    similarity: float
    foliage: float
    crop_index: int
    reason: str
    fruit_score: float = 0.0
    leaf_prob: float = 0.0


def foliage_fraction(rgb: np.ndarray) -> float:
    """Share of pixels that look like leaf tissue, including diseased colors."""
    rgb_u8 = np.clip(rgb, 0, 255).astype(np.uint8)
    r = rgb_u8[..., 0].astype(np.int16)
    g = rgb_u8[..., 1].astype(np.int16)
    b = rgb_u8[..., 2].astype(np.int16)
    hsv = np.asarray(Image.fromarray(rgb_u8, mode="RGB").convert("HSV"))
    h = hsv[..., 0].astype(np.int16)
    s = hsv[..., 1].astype(np.int16)
    v = hsv[..., 2].astype(np.int16)

    healthy_green = (g > r + 8) & (g > b + 8) & (s >= 28) & (v >= 25)
    yellow_chlorosis = (h >= 22) & (h <= 70) & (s >= 35) & (v >= 40)
    brown_necrosis = (
        (h >= 8)
        & (h <= 32)
        & (s >= 30)
        & (v >= 25)
        & (v <= 190)
        & (r <= g + 18)
        & (r > b + 8)
    )
    plant = healthy_green | yellow_chlorosis | brown_necrosis
    return float(np.mean(plant))


def round_fruit_score(rgb: np.ndarray) -> float:
    """Largest round red/yellow blob as a fraction of the frame.

    Ripe tomatoes are smooth ellipses. Bronzed or chlorotic leaflets are
    irregular, so they score near zero even when they are orange or yellow.
    """
    import cv2

    rgb_u8 = np.clip(rgb, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(rgb_u8, cv2.COLOR_RGB2HSV)
    hue, sat, val = cv2.split(hsv)
    red = ((hue <= 10) | (hue >= 170)) & (sat >= 80) & (val >= 50)
    yellow = (hue >= 12) & (hue <= 38) & (sat >= 90) & (val >= 70)
    r = rgb_u8[:, :, 0].astype(np.int16)
    g = rgb_u8[:, :, 1].astype(np.int16)
    not_leaf_green = g <= r + 12
    mask = ((red | yellow) & not_leaf_green).astype(np.uint8) * 255
    mask = cv2.medianBlur(mask, 5)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    )
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    height, width = mask.shape
    image_area = float(max(height * width, 1))
    best = 0.0
    for contour in contours:
        area = float(cv2.contourArea(contour))
        if area < 0.04 * image_area:
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter < 1:
            continue
        circularity = float(4.0 * np.pi * area / (perimeter * perimeter))
        (_center), radius = cv2.minEnclosingCircle(contour)
        circle_area = float(np.pi * radius * radius)
        fill = area / max(circle_area, 1.0)
        if circularity > 0.45 and fill > 0.55:
            best = max(best, area / image_area)
    return float(best)


def l2_normalize(vectors: np.ndarray, axis: int = -1) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=axis, keepdims=True)
    return vectors / np.clip(norms, 1e-8, None)


def embedding_model(keras_model):
    import tensorflow as tf

    try:
        pooled = keras_model.get_layer("avg_pool").output
    except ValueError:
        pooled = next(
            layer.output
            for layer in keras_model.layers
            if isinstance(layer, tf.keras.layers.GlobalAveragePooling2D)
        )
    return tf.keras.Model(keras_model.input, pooled, name="leaf_embed")


def export_embedding_tflite(keras_model, tflite_path: str) -> None:
    import tensorflow as tf

    embed_model = embedding_model(keras_model)
    converter = tf.lite.TFLiteConverter.from_keras_model(embed_model)
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


def run_embeddings(interpreter, batch: np.ndarray) -> np.ndarray:
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    vectors = []
    for sample in batch:
        tensor = np.expand_dims(sample, axis=0)
        if input_details["dtype"] == np.uint8:
            scale, zero_point = input_details.get("quantization", (0.0, 0))
            if scale:
                tensor = tensor / scale + zero_point
            tensor = np.clip(tensor, 0, 255).astype(np.uint8)
        else:
            tensor = tensor.astype(input_details["dtype"])
        interpreter.set_tensor(input_details["index"], tensor)
        interpreter.invoke()
        vectors.append(interpreter.get_tensor(output_details["index"])[0])
    return np.stack(vectors, axis=0).astype(np.float32)


def load_gate_artifacts(model_dir: str = config.MODEL_DIR) -> dict:
    path = os.path.join(model_dir, config.LEAF_GATE_NAME)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    payload = np.load(path)
    gallery = (
        payload["gallery"].astype(np.float32)
        if "gallery" in payload.files
        else payload["prototype"].reshape(1, -1).astype(np.float32)
    )
    fruit_gallery = (
        payload["fruit_gallery"].astype(np.float32)
        if "fruit_gallery" in payload.files
        else np.zeros((0, gallery.shape[-1]), dtype=np.float32)
    )
    coef = payload["leaf_coef"].astype(np.float32) if "leaf_coef" in payload.files else None
    intercept = float(payload["leaf_intercept"]) if "leaf_intercept" in payload.files else 0.0
    fruit_max = (
        float(payload["fruit_blob_max"])
        if "fruit_blob_max" in payload.files
        else float(config.LEAF_FRUIT_BLOB_MAX)
    )
    prob_min = (
        float(payload["leaf_prob_min"])
        if "leaf_prob_min" in payload.files
        else float(config.LEAF_PROB_MIN)
    )
    return {
        "gallery": l2_normalize(gallery),
        "fruit_gallery": l2_normalize(fruit_gallery) if len(fruit_gallery) else fruit_gallery,
        "leaf_coef": coef,
        "leaf_intercept": intercept,
        "similarity_threshold": float(payload["similarity_threshold"]),
        "foliage_min": float(payload["foliage_min"]),
        "fruit_blob_max": fruit_max,
        "leaf_prob_min": prob_min,
    }


def _center_views(image: Image.Image, image_size: int) -> np.ndarray:
    crop = square_crop_resize(image, image_size, offset=0.5)
    flipped = np.ascontiguousarray(np.fliplr(crop))
    return np.stack([crop, flipped], axis=0).astype(np.float32), crop


def _sigmoid(logits: np.ndarray) -> np.ndarray:
    clipped = np.clip(logits, -20.0, 20.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def leaf_probability(embedding: np.ndarray, gate: dict) -> float:
    coef = gate.get("leaf_coef")
    if coef is None:
        return 1.0
    logit = float(np.dot(embedding.reshape(-1), coef.reshape(-1)) + float(gate["leaf_intercept"]))
    return float(_sigmoid(np.array([logit]))[0])


def evaluate_tomato_leaf(
    image: Image.Image,
    embed_interpreter,
    gate: dict,
    image_size: int = config.IMG_SIZE,
    use_tta: bool = False,
) -> LeafGateResult:
    del use_tta  # Gate always uses the center crop; TTA is for disease scoring only.
    batch, crop = _center_views(image, image_size)
    embeddings = l2_normalize(run_embeddings(embed_interpreter, batch))
    embedding = l2_normalize(embeddings.mean(axis=0, keepdims=True))[0]
    gallery = l2_normalize(np.asarray(gate["gallery"], dtype=np.float32))
    similarity = float((embedding @ gallery.T).max())
    fruit_gallery = gate.get("fruit_gallery")
    fruit_similarity = -1.0
    if fruit_gallery is not None and len(fruit_gallery):
        fruit_similarity = float((embedding @ l2_normalize(np.asarray(fruit_gallery, dtype=np.float32)).T).max())
    foliage = foliage_fraction(crop)
    fruit_score = round_fruit_score(crop)
    probability = leaf_probability(embedding, gate)

    if fruit_score >= float(gate.get("fruit_blob_max", config.LEAF_FRUIT_BLOB_MAX)):
        return LeafGateResult(False, similarity, foliage, 0, "fruit", fruit_score, probability)
    if fruit_similarity >= 0 and fruit_similarity >= similarity - 0.02 and fruit_similarity >= 0.35:
        return LeafGateResult(False, similarity, foliage, 0, "fruit", fruit_score, probability)
    if foliage < float(gate["foliage_min"]):
        return LeafGateResult(False, similarity, foliage, 0, "not_leaf_tissue", fruit_score, probability)
    if probability < float(gate.get("leaf_prob_min", config.LEAF_PROB_MIN)):
        return LeafGateResult(False, similarity, foliage, 0, "not_tomato_leaf", fruit_score, probability)
    if similarity < float(gate["similarity_threshold"]):
        return LeafGateResult(False, similarity, foliage, 0, "not_tomato_leaf", fruit_score, probability)
    return LeafGateResult(True, similarity, foliage, 0, "tomato_leaf", fruit_score, probability)


def reject_message(result: LeafGateResult) -> str:
    if result.reason == "fruit":
        return (
            "This photo looks like tomato fruit (or another round object), not a tomato leaf. "
            "Upload a close-up of a single tomato leaflet filling the frame."
        )
    if result.reason == "not_leaf_tissue":
        return (
            "This photo does not look like a tomato leaf. Upload a close-up of a "
            "tomato leaflet filling the frame — not fruit, people, soil, or documents."
        )
    return (
        "This photo does not match a tomato leaf closely enough to scan. "
        "Use a sharper close-up of a single tomato leaflet under even light."
    )


def _synthetic_negatives(size: int = config.IMG_SIZE) -> list[np.ndarray]:
    images: list[np.ndarray] = []
    rng = np.random.RandomState(config.SEED)
    fruit_colors = [
        (220, 40, 35),
        (200, 25, 20),
        (230, 90, 30),
        (235, 185, 40),
        (240, 210, 70),
        (180, 20, 30),
        (90, 150, 40),
        (40, 140, 50),
    ]
    backgrounds = [(18, 90, 22), (40, 40, 40), (210, 210, 200), (120, 90, 60), (255, 255, 255)]
    for color in fruit_colors:
        for bg in backgrounds:
            canvas = Image.new("RGB", (640, 480), bg)
            draw = ImageDraw.Draw(canvas)
            draw.ellipse((140, 40, 520, 440), fill=color)
            draw.polygon([(310, 20), (340, 70), (280, 70)], fill=(30, 110, 40))
            images.append(square_crop_resize(canvas, size, 0.5))
            images.append(square_crop_resize(canvas, size, 0.0))
            images.append(square_crop_resize(canvas, size, 1.0))
    for _ in range(8):
        noise = Image.fromarray(rng.randint(0, 255, (size, size, 3), dtype=np.uint8))
        images.append(np.asarray(noise, dtype=np.float32))
    for rgb in [(190, 145, 120), (245, 245, 245), (20, 20, 20), (30, 80, 180), (200, 40, 35), (230, 190, 40)]:
        images.append(np.full((size, size, 3), rgb, dtype=np.float32))
    return images


def _is_fruit_like_path(path: str, crop: np.ndarray) -> bool:
    name = os.path.basename(path).lower()
    if any(hint in name for hint in ("rotating-tomato", "tomato-plants", "on-vine", "tomatoes-on-vine")):
        return True
    return round_fruit_score(crop) >= float(config.LEAF_FRUIT_BLOB_MAX)


def build_and_save_leaf_gate(
    keras_model,
    image_paths: list[str],
    model_dir: str = config.MODEL_DIR,
    export_embed: bool = True,
) -> dict:
    """Fit leaflet gallery + fruit rejector and export embed TFLite."""
    from sklearn.linear_model import LogisticRegression

    os.makedirs(model_dir, exist_ok=True)
    embed = embedding_model(keras_model)
    leaflet_crops: list[np.ndarray] = []
    fruit_crops: list[np.ndarray] = []
    for path in image_paths:
        with Image.open(path) as image:
            crop = square_crop_resize(to_rgb(image), config.IMG_SIZE, 0.5)
        if _is_fruit_like_path(path, crop):
            fruit_crops.append(crop)
            for offset in (0.0, 1.0):
                with Image.open(path) as image:
                    fruit_crops.append(square_crop_resize(to_rgb(image), config.IMG_SIZE, offset))
        else:
            leaflet_crops.append(crop)

    if not leaflet_crops:
        raise RuntimeError("No tomato leaflet images found to build the leaf gate.")

    leaflet_batch = np.stack(leaflet_crops, axis=0).astype(np.float32)
    leaflet_vectors = l2_normalize(embed.predict(leaflet_batch, batch_size=config.BATCH_SIZE, verbose=0).astype(np.float32))
    pairwise = leaflet_vectors @ leaflet_vectors.T
    np.fill_diagonal(pairwise, -1.0)
    loo_similarities = pairwise.max(axis=1)
    foliage = np.array([foliage_fraction(crop) for crop in leaflet_crops], dtype=np.float32)
    prototype = l2_normalize(leaflet_vectors.mean(axis=0, keepdims=True))[0]

    negative_crops = fruit_crops + _synthetic_negatives()
    negative_batch = np.stack(negative_crops, axis=0).astype(np.float32)
    negative_vectors = l2_normalize(embed.predict(negative_batch, batch_size=config.BATCH_SIZE, verbose=0).astype(np.float32))

    features = np.concatenate([leaflet_vectors, negative_vectors], axis=0)
    labels = np.concatenate(
        [np.ones(len(leaflet_vectors), dtype=np.int32), np.zeros(len(negative_vectors), dtype=np.int32)]
    )
    classifier = LogisticRegression(class_weight="balanced", max_iter=400, solver="lbfgs")
    classifier.fit(features, labels)
    positive_scores = classifier.predict_proba(leaflet_vectors)[:, 1]
    raw_prob_min = float(np.percentile(positive_scores, 2) - 0.08)
    leaf_prob_min = float(np.clip(raw_prob_min, 0.45, 0.70))

    fruit_gallery = negative_vectors[: max(len(fruit_crops), 1)] if fruit_crops else negative_vectors[:8]

    raw_threshold = float(np.percentile(loo_similarities, 2) - 0.06)
    similarity_threshold = float(np.clip(raw_threshold, config.LEAF_SIMILARITY_FLOOR, 0.48))
    foliage_min = float(config.LEAF_FOLIAGE_FLOOR)
    fruit_blob_max = float(config.LEAF_FRUIT_BLOB_MAX)

    embed_path = os.path.join(model_dir, config.LEAF_EMBED_TFLITE_NAME)
    gate_path = os.path.join(model_dir, config.LEAF_GATE_NAME)
    if export_embed or not os.path.exists(embed_path):
        export_embedding_tflite(keras_model, embed_path)
    np.savez(
        gate_path,
        gallery=leaflet_vectors.astype(np.float32),
        fruit_gallery=fruit_gallery.astype(np.float32),
        prototype=prototype.astype(np.float32),
        leaf_coef=classifier.coef_.reshape(-1).astype(np.float32),
        leaf_intercept=np.float32(classifier.intercept_[0]),
        similarity_threshold=np.float32(similarity_threshold),
        foliage_min=np.float32(foliage_min),
        fruit_blob_max=np.float32(fruit_blob_max),
        leaf_prob_min=np.float32(leaf_prob_min),
        train_similarity_min=np.float32(np.min(loo_similarities)),
        train_similarity_mean=np.float32(np.mean(loo_similarities)),
        train_foliage_min=np.float32(np.min(foliage)),
        sample_count=np.int32(len(leaflet_crops)),
    )
    stats = {
        "embed_path": embed_path,
        "gate_path": gate_path,
        "similarity_threshold": similarity_threshold,
        "foliage_min": foliage_min,
        "leaf_prob_min": leaf_prob_min,
        "fruit_blob_max": fruit_blob_max,
        "train_similarity_min": float(np.min(loo_similarities)),
        "train_similarity_mean": float(np.mean(loo_similarities)),
        "train_foliage_min": float(np.min(foliage)),
        "sample_count": len(leaflet_crops),
        "fruit_negatives": len(fruit_crops),
    }
    print(
        "Leaf gate: "
        f"leaflets={stats['sample_count']} fruit_negs={stats['fruit_negatives']} "
        f"sim_mean={stats['train_similarity_mean']:.3f} "
        f"threshold={similarity_threshold:.3f} "
        f"prob_min={leaf_prob_min:.3f} "
        f"fruit_blob_max={fruit_blob_max:.3f}"
    )
    return stats


def main() -> None:
    import tensorflow as tf

    from data_utils import list_image_records, prepare_dataset

    keras_path = os.path.join(config.MODEL_DIR, config.KERAS_MODEL_NAME)
    if not os.path.exists(keras_path):
        raise SystemExit("Train the Keras model first: python train.py")
    prepare_dataset()
    train_paths, _ = list_image_records(config.READY_TRAIN_DIR)
    val_paths, _ = list_image_records(config.READY_VAL_DIR)
    model = tf.keras.models.load_model(keras_path)
    embed_path = os.path.join(config.MODEL_DIR, config.LEAF_EMBED_TFLITE_NAME)
    build_and_save_leaf_gate(
        model,
        train_paths + val_paths,
        export_embed=not os.path.exists(embed_path),
    )


if __name__ == "__main__":
    main()
