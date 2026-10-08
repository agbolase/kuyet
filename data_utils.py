"""Dataset cleanup, class alignment, and tf.data pipelines."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from sklearn.utils.class_weight import compute_class_weight

import config
from image_prep import square_crop_resize

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"}


def normalize_class_key(name: str) -> str:
    key = name.strip().lower().replace("-", "_").replace(" ", "_")
    return re.sub(r"_+", "_", key)


def canonical_class_name(folder_name: str) -> str:
    key = normalize_class_key(folder_name)
    if key not in config.CLASS_ALIASES:
        raise ValueError(
            f"Unknown class folder '{folder_name}'. Add a mapping in config.CLASS_ALIASES."
        )
    return config.CLASS_ALIASES[key]


def _stem_without_image_suffix(filename: str) -> str:
    name = filename
    lowered = name.lower()
    for ext in [".jpg.webp", ".jpeg.webp", ".png.webp", ".webp", ".jpeg", ".jpg", ".png", ".bmp", ".gif", ".tiff", ".tif"]:
        if lowered.endswith(ext):
            return name[: -len(ext)]
    return Path(filename).stem


def _convert_to_rgb_jpeg(src: Path, dst: Path) -> None:
    with Image.open(src) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        dst.parent.mkdir(parents=True, exist_ok=True)
        image.save(dst, format="JPEG", quality=95, optimize=True)


def _count_ready_images() -> dict[str, int]:
    counts: dict[str, int] = {}
    for ready_root in (config.READY_TRAIN_DIR, config.READY_VAL_DIR):
        root = Path(ready_root)
        if not root.exists():
            return {}
        for class_name in config.CLASS_NAMES:
            folder = root / class_name
            n = len(list(folder.glob("*.jpg"))) if folder.is_dir() else 0
            counts[f"{root.name}/{class_name}"] = n
    return counts


def _ready_dataset_complete() -> bool:
    counts = _count_ready_images()
    return bool(counts) and all(value > 0 for value in counts.values())


def prepare_dataset(force: bool = False) -> dict[str, int]:
    """Rewrite train/val folders with aligned class names and JPEG RGB images.

    Keras directory loaders skip WebP. Train and validation folders in this
    project also used different spellings, so integer labels did not match.
    """
    if not force and _ready_dataset_complete():
        return _count_ready_images()

    counts: dict[str, int] = {}
    for raw_root, ready_root in (
        (config.RAW_TRAIN_DIR, config.READY_TRAIN_DIR),
        (config.RAW_VAL_DIR, config.READY_VAL_DIR),
    ):
        ready_path = Path(ready_root)
        if ready_path.exists():
            shutil.rmtree(ready_path)
        for class_dir in sorted(Path(raw_root).iterdir()):
            if not class_dir.is_dir():
                continue
            canonical = canonical_class_name(class_dir.name)
            destination_dir = ready_path / canonical
            destination_dir.mkdir(parents=True, exist_ok=True)
            for src in sorted(class_dir.iterdir()):
                if not src.is_file() or src.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                dst = destination_dir / f"{_stem_without_image_suffix(src.name)}.jpg"
                if dst.exists():
                    dst = destination_dir / f"{dst.stem}_{src.stat().st_ino}.jpg"
                _convert_to_rgb_jpeg(src, dst)
                counts[f"{Path(ready_root).name}/{canonical}"] = (
                    counts.get(f"{Path(ready_root).name}/{canonical}", 0) + 1
                )
    return counts


def list_image_records(split_dir: str) -> tuple[list[str], list[int]]:
    class_to_index = {name: idx for idx, name in enumerate(config.CLASS_NAMES)}
    paths: list[str] = []
    labels: list[int] = []
    split_path = Path(split_dir)
    for class_name in config.CLASS_NAMES:
        class_dir = split_path / class_name
        if not class_dir.is_dir():
            raise FileNotFoundError(f"Missing class folder: {class_dir}")
        images = sorted(class_dir.glob("*.jpg"))
        if not images:
            raise FileNotFoundError(f"No JPEG images found in {class_dir}")
        for image_path in images:
            paths.append(str(image_path))
            labels.append(class_to_index[class_name])
    return paths, labels


def load_square_images(paths: list[str], size: int) -> np.ndarray:
    images = []
    for path in paths:
        with Image.open(path) as image:
            images.append(square_crop_resize(image, size))
    return np.stack(images, axis=0).astype(np.float32)


def compute_balanced_class_weights(labels: list[int]) -> dict[int, float]:
    weights = compute_class_weight(
        class_weight="balanced",
        classes=np.arange(len(config.CLASS_NAMES)),
        y=np.array(labels),
    )
    return {idx: float(weight) for idx, weight in enumerate(weights)}


def save_model_metadata(extra: dict | None = None) -> str:
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    metadata = {
        "classes": config.CLASS_NAMES,
        "display_names": config.DISPLAY_NAMES,
        "image_size": config.IMG_SIZE,
        "input_range": [0, 255],
        "letterbox": False,
        "crop": "square_cover",
        "architecture": config.ARCHITECTURE,
        "preprocess": "efficientnetv2_builtin",
    }
    if extra:
        metadata.update(extra)
    path = os.path.join(config.MODEL_DIR, config.METADATA_NAME)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)
    with open(config.METADATA_NAME, "w", encoding="utf-8") as handle:
        json.dump(config.CLASS_NAMES, handle, indent=2)
    return path
