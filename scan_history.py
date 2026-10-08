"""Persist and load completed leaf scan logs."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

import config

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "data" / "scan_logs"
HISTORY_PATH = LOG_DIR / "history.json"
THUMBS_DIR = LOG_DIR / "thumbs"
MAX_ENTRIES = 500
THUMB_SIZE = (120, 120)


def _ensure_dirs() -> None:
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)


def load_entries() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    try:
        with open(HISTORY_PATH, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(payload, list):
        return []
    return payload


def _save_entries(entries: list[dict]) -> None:
    _ensure_dirs()
    with open(HISTORY_PATH, "w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)


def _save_thumbnail(entry_id: str, crop: np.ndarray) -> str:
    _ensure_dirs()
    array = np.asarray(crop)
    if array.dtype != np.uint8:
        array = (np.clip(array, 0, 1) * 255).astype(np.uint8)
    image = Image.fromarray(array)
    image.thumbnail(THUMB_SIZE, Image.Resampling.LANCZOS)
    relative = f"thumbs/{entry_id}.jpg"
    image.save(THUMBS_DIR / f"{entry_id}.jpg", format="JPEG", quality=85)
    return relative


def thumb_path(relative: str) -> Path:
    return LOG_DIR / relative


def record_scan(
    *,
    predicted_key: str,
    confidence: float,
    top_indices: list[int],
    probabilities: np.ndarray,
    class_labels: list[str],
    display_names: dict,
    crop: np.ndarray,
    lang: str,
    use_tta: bool,
    source_name: str | None = None,
) -> dict:
    entry_id = str(uuid.uuid4())
    at = datetime.now(timezone.utc).isoformat()
    top3 = []
    for index in top_indices[:3]:
        key = class_labels[index]
        top3.append(
            {
                "key": key,
                "label": display_names.get(key, key.replace("_", " ")),
                "score": round(float(probabilities[index]), 4),
            }
        )
    thumb_rel = _save_thumbnail(entry_id, crop)
    entry = {
        "id": entry_id,
        "at": at,
        "predicted_key": predicted_key,
        "label": display_names.get(predicted_key, predicted_key.replace("_", " ")),
        "confidence": round(float(confidence), 4),
        "top3": top3,
        "lang": lang,
        "use_tta": use_tta,
        "source_name": source_name or "",
        "thumb": thumb_rel,
        "low_confidence": float(confidence) < config.CONFIDENCE_WARN_THRESHOLD,
    }
    entries = load_entries()
    entries.insert(0, entry)
    _save_entries(entries[:MAX_ENTRIES])
    return entry


def clear_history() -> None:
    for path in THUMBS_DIR.glob("*.jpg"):
        path.unlink(missing_ok=True)
    if HISTORY_PATH.exists():
        HISTORY_PATH.unlink()
