#!/usr/bin/env python3
"""Bundle models and field guides for the offline Android app."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOBILE_ASSETS = ROOT / "mobile" / "assets"
MODEL_SRC = ROOT / "models"
MODEL_DST = MOBILE_ASSETS / "models"
GUIDE_DST = MOBILE_ASSETS / "guides"

MODEL_FILES = (
    "hortivision_model.tflite",
    "leaf_embed.tflite",
    "leaf_gate.npz",
    "class_names.json",
)


def export_guides() -> None:
    import disease_guide
    import disease_guide_ha

    GUIDE_DST.mkdir(parents=True, exist_ok=True)
    (GUIDE_DST / "disease_guide_en.json").write_text(
        json.dumps(disease_guide.DISEASE_GUIDE, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (GUIDE_DST / "disease_guide_ha.json").write_text(
        json.dumps(disease_guide_ha.DISEASE_GUIDE_HA, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def copy_models() -> list[str]:
    MODEL_DST.mkdir(parents=True, exist_ok=True)
    missing: list[str] = []
    for name in MODEL_FILES:
        src = MODEL_SRC / name
        dst = MODEL_DST / name
        if src.is_file():
            shutil.copy2(src, dst)
        else:
            missing.append(name)
    return missing


def main() -> int:
    export_guides()
    missing = copy_models()
    print(f"Guides exported to {GUIDE_DST}")
    print(f"Models directory: {MODEL_DST}")
    if missing:
        print(
            "WARNING: missing model files (APK will install but scan needs these):",
            ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "Train/export on the server project, then re-run this script.",
            file=sys.stderr,
        )
        return 1
    print("All mobile assets ready.")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
