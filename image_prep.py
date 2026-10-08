"""Image preprocessing shared by the app and evaluation."""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageOps


def to_rgb(image: Image.Image) -> Image.Image:
    return ImageOps.exif_transpose(image).convert("RGB")


def square_crop_resize(image: Image.Image, size: int, offset: float = 0.5) -> np.ndarray:
    """Fill the model window with leaf tissue instead of padding with black bars.

    offset 0 is the start of the long axis, 0.5 is center, 1.0 is the end.
    """
    image = to_rgb(image)
    width, height = image.size
    side = min(width, height)
    if width >= height:
        left = int(round((width - side) * offset))
        left = max(0, min(left, width - side))
        box = (left, 0, left + side, side)
    else:
        top = int(round((height - side) * offset))
        top = max(0, min(top, height - side))
        box = (0, top, side, top + side)
    crop = image.crop(box)
    return np.asarray(crop.resize((size, size), Image.Resampling.BILINEAR), dtype=np.float32)


def crop_offsets(image: Image.Image) -> tuple[float, ...]:
    image = to_rgb(image)
    width, height = image.size
    ratio = max(width, height) / max(min(width, height), 1)
    if ratio >= 1.35:
        return (0.0, 0.5, 1.0)
    return (0.5,)


def inference_views(
    image: Image.Image,
    size: int,
    use_tta: bool = True,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """Build square crops (plus optional horizontal flips) for inference."""
    offsets = crop_offsets(image) if use_tta else (0.5,)
    crops: list[np.ndarray] = []
    tensors: list[np.ndarray] = []
    for offset in offsets:
        crop = square_crop_resize(image, size, offset)
        crops.append(crop)
        tensors.append(crop)
        if use_tta:
            tensors.append(np.ascontiguousarray(np.fliplr(crop)))
    return np.stack(tensors, axis=0).astype(np.float32), crops


def select_best_prediction(
    view_probabilities: np.ndarray,
    crop_count: int,
    views_per_crop: int,
) -> tuple[np.ndarray, int]:
    """Average flips per crop, then keep the most decisive crop."""
    grouped = view_probabilities.reshape(crop_count, views_per_crop, -1).mean(axis=1)
    best_crop = int(np.argmax(grouped.max(axis=1)))
    return grouped[best_crop], best_crop


def sharpen_probabilities(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    """Peak the softmax without changing the predicted class ranking.

    The 11-class head spreads leftover mass across similar diseases, which
    made even a correct leaf read as ~30% confident.
    """
    if temperature <= 0 or temperature >= 1:
        return probabilities
    logits = np.log(np.clip(probabilities, 1e-8, 1.0))
    logits = logits / temperature
    logits = logits - np.max(logits, axis=-1, keepdims=True)
    exp = np.exp(logits)
    return exp / np.sum(exp, axis=-1, keepdims=True)
