"""Evaluate the saved TFLite model on the aligned validation set."""

from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix

import config
from data_utils import list_image_records, prepare_dataset
from image_prep import inference_views, select_best_prediction, sharpen_probabilities


def run_views(interpreter, batch: np.ndarray) -> np.ndarray:
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    probs = []
    for sample in batch:
        tensor = np.expand_dims(sample, axis=0).astype(input_details["dtype"])
        interpreter.set_tensor(input_details["index"], tensor)
        interpreter.invoke()
        probs.append(interpreter.get_tensor(output_details["index"])[0])
    return np.stack(probs, axis=0)


def predict_image(interpreter, image: Image.Image, image_size: int) -> np.ndarray:
    batch, crops = inference_views(image, image_size, use_tta=True)
    views = run_views(interpreter, batch)
    probabilities, _ = select_best_prediction(views, len(crops), 2)
    return sharpen_probabilities(probabilities, config.SOFTMAX_TEMPERATURE)


def main() -> None:
    import tensorflow as tf

    model_path = os.path.join(config.MODEL_DIR, config.TFLITE_MODEL_NAME)
    labels_path = os.path.join(config.MODEL_DIR, config.METADATA_NAME)
    if not os.path.exists(model_path):
        raise SystemExit("No TFLite model found. Train first with python train.py")

    prepare_dataset()
    paths, labels = list_image_records(config.READY_VAL_DIR)
    with open(labels_path, encoding="utf-8") as handle:
        metadata = json.load(handle)
    class_names = metadata["classes"] if isinstance(metadata, dict) else metadata
    image_size = int(metadata.get("image_size", config.IMG_SIZE)) if isinstance(metadata, dict) else config.IMG_SIZE

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    y_pred = []
    confidences = []
    for path in paths:
        with Image.open(path) as image:
            probabilities = predict_image(interpreter, image, image_size)
        y_pred.append(int(np.argmax(probabilities)))
        confidences.append(float(np.max(probabilities)))

    y_true = np.array(labels)
    y_pred = np.array(y_pred)
    accuracy = float(np.mean(y_true == y_pred))
    print(f"Validation images: {len(paths)}")
    print(f"Mean confidence: {np.mean(confidences):.4f}")
    print(f"Accuracy: {accuracy:.4f}\n")
    print(
        classification_report(
            y_true,
            y_pred,
            target_names=class_names,
            digits=4,
            zero_division=0,
        )
    )
    print("Confusion matrix")
    print(confusion_matrix(y_true, y_pred))


if __name__ == "__main__":
    main()
