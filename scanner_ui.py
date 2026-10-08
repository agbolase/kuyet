"""TomatoCare leaf scanner UI (Streamlit)."""

from __future__ import annotations

import hashlib
import importlib
import json
import os

import numpy as np
import streamlit as st
from PIL import Image

import config
import scan_history
import disease_guide as _disease_guide
import disease_guide_ha as _disease_guide_ha
import image_prep as _image_prep
import leaf_gate as _leaf_gate
import speech as _speech
import translations as _translations

_image_prep = importlib.reload(_image_prep)
_disease_guide_ha = importlib.reload(_disease_guide_ha)
_disease_guide = importlib.reload(_disease_guide)
_leaf_gate = importlib.reload(_leaf_gate)
_speech = importlib.reload(_speech)
_translations = importlib.reload(_translations)
disease_guide = _disease_guide
leaf_gate = _leaf_gate
speech = _speech
t = _translations.t
inference_views = _image_prep.inference_views
select_best_prediction = _image_prep.select_best_prediction


def sharpen_probabilities(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    if temperature <= 0 or temperature >= 1:
        return probabilities
    logits = np.log(np.clip(probabilities, 1e-8, 1.0)) / temperature
    logits = logits - np.max(logits, axis=-1, keepdims=True)
    exp = np.exp(logits)
    return exp / np.sum(exp, axis=-1, keepdims=True)


MODEL_PATH = os.path.join(config.MODEL_DIR, config.TFLITE_MODEL_NAME)
LABELS_PATH = os.path.join(config.MODEL_DIR, config.METADATA_NAME)
LEAF_EMBED_PATH = os.path.join(config.MODEL_DIR, config.LEAF_EMBED_TFLITE_NAME)
LEAF_GATE_PATH = os.path.join(config.MODEL_DIR, config.LEAF_GATE_NAME)


def load_metadata(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return {
            "classes": payload,
            "display_names": {name: name.replace("_", " ") for name in payload},
            "image_size": config.IMG_SIZE,
            "input_range": [0, 255],
            "letterbox": False,
        }
    return payload


@st.cache_resource
def load_interpreter(model_path: str, mtime: float):
    import tensorflow as tf

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


@st.cache_data(show_spinner=False, max_entries=64)
def synthesize_cached(text: str, lang: str) -> bytes:
    return speech.synthesize(text, lang)


def run_views(interpreter, batch: np.ndarray) -> np.ndarray:
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    probabilities = []
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
        probabilities.append(interpreter.get_tensor(output_details["index"])[0])
    return np.stack(probabilities, axis=0)


def current_language() -> str:
    return st.session_state.setdefault("lang", "en")


def toggle_language() -> None:
    st.session_state["lang"] = "ha" if current_language() == "en" else "en"


def class_name(class_key: str, lang: str, display_names: dict) -> str:
    if lang == "ha":
        return disease_guide.get_guide(class_key, "ha")["name"]
    return display_names.get(class_key, class_key.replace("_", " "))


def render_speech_button(text: str, lang: str) -> None:
    clicked = st.button(t("read_aloud", lang), key="read_aloud")
    if not (clicked or st.session_state.pop("speak_request", False)):
        return
    try:
        with st.spinner(t("preparing_audio", lang)):
            audio = synthesize_cached(speech.spoken_form(text, lang), lang)
    except speech.SpeechUnavailable:
        st.warning(t("speech_offline", lang))
        return
    st.audio(audio, format="audio/mp3", autoplay=True)


def handle_voice_commands(lang: str) -> None:
    st.markdown(f"**{t('voice_title', lang)}**")
    st.caption(t("voice_help", lang))
    recording = st.audio_input(
        "Voice command / Umarnin murya",
        key="voice_command",
        label_visibility="collapsed",
    )
    if recording is not None:
        data = recording.getvalue()
        digest = hashlib.sha1(data).hexdigest()
        if st.session_state.get("voice_digest") != digest:
            st.session_state["voice_digest"] = digest
            try:
                with st.spinner(t("voice_listening", lang)):
                    heard, command = speech.transcribe_command(data, lang)
            except speech.SpeechUnavailable:
                st.session_state["voice_feedback"] = ("speech_offline", "")
                heard, command = "", None
            else:
                st.session_state["voice_feedback"] = (
                    ("voice_heard" if command else "voice_unknown") if heard else "voice_silent",
                    heard,
                )
            if command in ("hausa", "english"):
                target = "ha" if command == "hausa" else "en"
                if target != lang:
                    st.session_state["lang"] = target
                    st.rerun()
            elif command == "read":
                st.session_state["speak_request"] = True
            elif command == "scan":
                st.session_state["scan_request"] = True

    feedback = st.session_state.get("voice_feedback")
    if feedback:
        key, heard = feedback
        if key == "voice_heard":
            st.caption(t("voice_heard", lang, text=heard))
        else:
            if heard:
                st.caption(t("voice_heard", lang, text=heard))
            st.warning(t(key, lang))


def render_disease_profile(class_key: str, confidence: float, lang: str) -> None:
    guide = disease_guide.get_guide(class_key, lang)
    st.subheader(t("advisory", lang))
    if confidence < config.CONFIDENCE_WARN_THRESHOLD:
        st.caption(t("advisory_tentative", lang))
    st.write(guide["summary"])

    st.markdown(f"**{t('causal_agent', lang)}:** {guide['agent_type']} — {guide['agent']}")

    st.markdown(f"**{t('traits', lang)}**")
    for trait in guide["traits"]:
        st.write(f"- {trait}")

    st.markdown(f"**{t('prevention', lang)}**")
    for step in guide["prevention"]:
        st.write(f"- {step}")

    st.caption(t("disclaimer", lang))
    note = t("translation_note", lang)
    if note:
        st.caption(note)


def result_speech_text(scan: dict, lang: str, display_names: dict) -> str:
    key = scan["predicted_key"]
    guide = disease_guide.get_guide(key, lang)
    parts = [
        t(
            "speech_result",
            lang,
            name=class_name(key, lang, display_names),
            confidence=int(round(scan["confidence"] * 100)),
        )
    ]
    if scan["confidence"] < config.CONFIDENCE_WARN_THRESHOLD:
        parts.append(t("speech_low_confidence", lang))
    parts.append(guide["summary"])
    parts.append(f"{t('causal_agent', lang)}: {guide['agent_type']}.")
    if guide["traits"]:
        parts.append(f"{t('traits', lang)}: " + ". ".join(guide["traits"]) + ".")
    if guide["prevention"]:
        parts.append(f"{t('prevention', lang)}: " + ". ".join(guide["prevention"]) + ".")
    return " ".join(parts)


def run_scan(image: Image.Image, image_size: int, use_tta: bool, class_labels: list) -> dict:
    interpreter = load_interpreter(MODEL_PATH, os.path.getmtime(MODEL_PATH))
    batch, crops = inference_views(image, image_size, use_tta=use_tta)
    views_per_crop = 2 if use_tta else 1
    view_probabilities = run_views(interpreter, batch)
    probabilities, best_crop = select_best_prediction(
        view_probabilities, len(crops), views_per_crop
    )
    probabilities = sharpen_probabilities(probabilities, config.SOFTMAX_TEMPERATURE)
    top_indices = [int(index) for index in np.argsort(probabilities)[::-1][:3]]
    predicted_index = top_indices[0]
    return {
        "probabilities": probabilities,
        "top_indices": top_indices,
        "predicted_key": class_labels[predicted_index],
        "confidence": float(probabilities[predicted_index]),
        "crop": crops[best_crop],
    }


def render_result(scan: dict, lang: str, class_labels: list, display_names: dict) -> None:
    confidence = scan["confidence"]
    st.image(
        (scan["crop"] / 255.0).clip(0, 1),
        caption=t("region_caption", lang),
        use_container_width=True,
    )
    name = class_name(scan["predicted_key"], lang, display_names)
    st.success(f"{t('prediction', lang)}: **{name}**")
    st.progress(min(max(confidence, 0.0), 1.0))
    st.info(f"{t('confidence', lang)}: **{confidence * 100:.2f}%**")

    if confidence < config.CONFIDENCE_WARN_THRESHOLD:
        st.warning(t("low_confidence", lang))

    st.subheader(t("top3", lang))
    for rank, index in enumerate(scan["top_indices"], start=1):
        key = class_labels[index]
        score = float(scan["probabilities"][index]) * 100
        st.write(f"{rank}. {class_name(key, lang, display_names)} — {score:.2f}%")

    render_disease_profile(scan["predicted_key"], confidence, lang)


def render_scanner() -> None:
    lang = current_language()

    title_col, button_col = st.columns([1.6, 1], vertical_alignment="center")
    title_col.markdown("### Scan a tomato leaf")
    title_col.caption(t("subtitle", lang))
    button_col.button(
        t("translate_button", lang),
        key="scan_translate_button",
        on_click=toggle_language,
        type="secondary",
        use_container_width=True,
    )

    if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
        st.warning(t("missing_model", lang))
        return
    if not os.path.exists(LEAF_EMBED_PATH) or not os.path.exists(LEAF_GATE_PATH):
        st.warning(t("missing_gate", lang))
        return

    metadata = load_metadata(LABELS_PATH)
    class_labels = metadata["classes"]
    display_names = metadata.get("display_names", {})
    image_size = int(metadata.get("image_size", config.IMG_SIZE))
    gate = leaf_gate.load_gate_artifacts(config.MODEL_DIR)

    with st.container(border=True):
        handle_voice_commands(lang)

    st.markdown(f"**{t('upload_label', lang)}**")
    uploaded_file = st.file_uploader(
        "Upload / Ɗora",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        key="leaf_upload",
        label_visibility="collapsed",
    )
    use_tta = st.checkbox(t("tta_label", lang), value=True, key="use_tta")

    if uploaded_file is None:
        st.session_state.pop("scan", None)
        if st.session_state.pop("scan_request", False):
            st.warning(t("voice_need_image", lang))
        st.caption(t("upload_hint", lang))
        render_speech_button(t("upload_hint", lang), lang)
        return

    image = Image.open(uploaded_file)
    st.image(image, caption=t("uploaded_caption", lang), use_container_width=True)

    cached_gate = st.session_state.get("gate_result")
    if cached_gate is not None and cached_gate[0] == uploaded_file.file_id:
        gate_result = cached_gate[1]
    else:
        with st.spinner(t("checking_leaf", lang)):
            embed_interpreter = load_interpreter(
                LEAF_EMBED_PATH, os.path.getmtime(LEAF_EMBED_PATH)
            )
            gate_result = leaf_gate.evaluate_tomato_leaf(
                image,
                embed_interpreter,
                gate,
                image_size=image_size,
            )
        st.session_state["gate_result"] = (uploaded_file.file_id, gate_result)

    if not gate_result.accepted:
        st.session_state.pop("scan", None)
        st.session_state.pop("scan_request", None)
        message = t(f"reject_{gate_result.reason}", lang)
        st.error(message)
        scores = t(
            "gate_scores",
            lang,
            similarity=gate_result.similarity * 100,
            foliage=gate_result.foliage * 100,
        )
        if gate_result.fruit_score > 0:
            scores += t("gate_fruit_score", lang, fruit=gate_result.fruit_score * 100)
        st.caption(scores)
        render_speech_button(message, lang)
        return

    st.caption(t("leaf_confirmed", lang))
    scan_id = (uploaded_file.file_id, use_tta)
    scan = st.session_state.get("scan")
    if scan is not None and scan.get("id") != scan_id:
        scan = None
        st.session_state.pop("scan", None)

    clicked = st.button(t("predict_button", lang), type="primary", key="predict_button")
    if clicked or st.session_state.pop("scan_request", False):
        with st.spinner(t("analyzing", lang)):
            scan = run_scan(image, image_size, use_tta, class_labels)
        scan["id"] = scan_id
        st.session_state["scan"] = scan
        scan_history.record_scan(
            predicted_key=scan["predicted_key"],
            confidence=scan["confidence"],
            top_indices=scan["top_indices"],
            probabilities=scan["probabilities"],
            class_labels=class_labels,
            display_names=display_names,
            crop=scan["crop"],
            lang=lang,
            use_tta=use_tta,
            source_name=getattr(uploaded_file, "name", None),
        )

    if scan is None:
        render_speech_button(t("leaf_confirmed", lang), lang)
        return

    render_result(scan, lang, class_labels, display_names)
    render_speech_button(result_speech_text(scan, lang, display_names), lang)

    architecture = metadata.get("architecture")
    if architecture:
        st.caption(t("model_caption", lang, architecture=architecture, size=image_size))
