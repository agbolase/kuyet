"""Shared training and inference settings for HORTIVISION-NG."""

from __future__ import annotations

SEED = 42
IMG_SIZE = 224
BATCH_SIZE = 8
PHASE1_EPOCHS = 20
PHASE2_EPOCHS = 30
FINE_TUNE_LAYER_FRACTION = 0.40
LABEL_SMOOTHING = 0.0
MIXUP_ALPHA = 0.0
DROPOUT = 0.2
WEIGHT_DECAY = 1e-4
PHASE1_LR = 1e-3
PHASE2_LR = 2e-5
AUGMENTED_VIEWS_PER_EPOCH = 128
ARCHITECTURE = "EfficientNetV2B0"

RAW_TRAIN_DIR = "dataset/train"
RAW_VAL_DIR = "dataset/validation"
READY_TRAIN_DIR = "dataset_ready/train"
READY_VAL_DIR = "dataset_ready/validation"
MODEL_DIR = "models"
KERAS_MODEL_NAME = "hortivision_model.keras"
TFLITE_MODEL_NAME = "hortivision_model.tflite"
LEAF_EMBED_TFLITE_NAME = "leaf_embed.tflite"
LEAF_GATE_NAME = "leaf_gate.npz"
METADATA_NAME = "class_names.json"
HISTORY_NAME = "training_history.json"

# Folder-name variants seen in this dataset, mapped to one canonical label.
CLASS_ALIASES = {
    "tomato_bacterial_spot": "Tomato_Bacterial_spot",
    "tomato_early_blight": "Tomato_Early_blight",
    "tomato_late_blight": "Tomato_Late_blight",
    "tomato_leaf_mold": "Tomato_Leaf_mold",
    "tomato_mosaic_virus": "Tomato_Mosaic_virus",
    "tomato_septoria_leaf_spot": "Tomato_Septoria_leaf_spot",
    "tomato_spider_mites_two_spotted_spider_mite": "Tomato_Spider_mites",
    "tomato_spider_mites_two_spotted_mite": "Tomato_Spider_mites",
    "tomato_target_spot": "Tomato_Target_spot",
    "tomato_yellow_leaf_curls_virus": "Tomato_Yellow_Leaf_Curl_Virus",
    "tomato_yellow_leaf_curl_virus": "Tomato_Yellow_Leaf_Curl_Virus",
    "tomato_bacterial_canker": "Tomato_Bacterial_canker",
    "tomato_healthy": "Tomato_healthy",
}

CLASS_NAMES = [
    "Tomato_Bacterial_canker",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_mold",
    "Tomato_Mosaic_virus",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites",
    "Tomato_Target_spot",
    "Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato_healthy",
]

DISPLAY_NAMES = {
    "Tomato_Bacterial_canker": "Bacterial Canker",
    "Tomato_Bacterial_spot": "Bacterial Spot",
    "Tomato_Early_blight": "Early Blight",
    "Tomato_Late_blight": "Late Blight",
    "Tomato_Leaf_mold": "Leaf Mold",
    "Tomato_Mosaic_virus": "Mosaic Virus",
    "Tomato_Septoria_leaf_spot": "Septoria Leaf Spot",
    "Tomato_Spider_mites": "Two-Spotted Spider Mites",
    "Tomato_Target_spot": "Target Spot",
    "Tomato_Yellow_Leaf_Curl_Virus": "Yellow Leaf Curl Virus",
    "Tomato_healthy": "Healthy",
}

CONFIDENCE_WARN_THRESHOLD = 0.50
SOFTMAX_TEMPERATURE = 0.45
# Cosine floor against the nearest tomato-leaf embedding; calibrated at export.
LEAF_SIMILARITY_FLOOR = 0.32
LEAF_FOLIAGE_FLOOR = 0.08
LEAF_FRUIT_BLOB_MAX = 0.08
LEAF_PROB_MIN = 0.55
