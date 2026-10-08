"""English and Hausa interface text for the HORTIVISION-NG app."""

from __future__ import annotations

LANGUAGES = ("en", "ha")

STRINGS = {
    "subtitle": {
        "en": "Offline tomato leaf disease detection",
        "ha": "Gano cututtukan ganyen tumatir ba tare da intanet ba",
    },
    "translate_button": {
        "en": "Fassara zuwa Hausa (Translate to Hausa)",
        "ha": "Koma Turanci (Switch to English)",
    },
    "missing_model": {
        "en": "Trained model files were not found. Run `python train.py` first.",
        "ha": "Ba a sami fayilolin na'urar da aka horar ba. Fara gudanar da `python train.py`.",
    },
    "missing_gate": {
        "en": "Tomato-leaf gate files were not found. Run `python leaf_gate.py` first.",
        "ha": "Ba a sami fayilolin tantance ganyen tumatir ba. Fara gudanar da `python leaf_gate.py`.",
    },
    "upload_label": {
        "en": "Upload a tomato leaf image",
        "ha": "Ɗora hoton ganyen tumatir",
    },
    "tta_label": {
        "en": "Scan multiple leaf regions (recommended)",
        "ha": "Duba sassan ganye da yawa (an ba da shawara)",
    },
    "upload_hint": {
        "en": "Use a close-up of a single leaf, with the damaged area filling the frame.",
        "ha": "Yi amfani da hoton ganye ɗaya a kusa, inda wurin da ya lalace ya cika hoton.",
    },
    "uploaded_caption": {
        "en": "Uploaded photo",
        "ha": "Hoton da aka ɗora",
    },
    "checking_leaf": {
        "en": "Checking that this is a tomato leaf...",
        "ha": "Ana tabbatar da cewa wannan ganyen tumatir ne...",
    },
    "leaf_confirmed": {
        "en": "Tomato leaf confirmed. You can scan for disease.",
        "ha": "An tabbatar ganyen tumatir ne. Za ka iya duba cuta.",
    },
    "gate_scores": {
        "en": "Leaf match {similarity:.1f}% · plant tissue {foliage:.1f}%",
        "ha": "Kamanceceniya da ganye {similarity:.1f}% · ɓangaren shuka {foliage:.1f}%",
    },
    "gate_fruit_score": {
        "en": " · fruit shape {fruit:.1f}%",
        "ha": " · siffar 'ya'yan itace {fruit:.1f}%",
    },
    "reject_fruit": {
        "en": (
            "This photo looks like tomato fruit (or another round object), not a tomato leaf. "
            "Upload a close-up of a single tomato leaflet filling the frame."
        ),
        "ha": (
            "Wannan hoton kamar 'ya'yan tumatir ne (ko wani abu mai zagaye), ba ganyen tumatir ba. "
            "Ɗora hoton ganyen tumatir ɗaya a kusa wanda ya cika hoton."
        ),
    },
    "reject_not_leaf_tissue": {
        "en": (
            "This photo does not look like a tomato leaf. Upload a close-up of a "
            "tomato leaflet filling the frame — not fruit, people, soil, or documents."
        ),
        "ha": (
            "Wannan hoton bai yi kama da ganyen tumatir ba. Ɗora hoton ganyen tumatir a kusa "
            "wanda ya cika hoton — ba 'ya'yan itace, mutane, ƙasa ko takardu ba."
        ),
    },
    "reject_not_tomato_leaf": {
        "en": (
            "This photo does not match a tomato leaf closely enough to scan. "
            "Use a sharper close-up of a single tomato leaflet under even light."
        ),
        "ha": (
            "Wannan hoton bai yi daidai da ganyen tumatir sosai ba. Yi amfani da hoto mai "
            "haske, a kusa, na ganyen tumatir ɗaya a cikin haske daidai."
        ),
    },
    "predict_button": {
        "en": "Predict disease",
        "ha": "Duba cuta",
    },
    "analyzing": {
        "en": "Analyzing leaf image...",
        "ha": "Ana nazarin hoton ganye...",
    },
    "region_caption": {
        "en": "Region analyzed by the model",
        "ha": "Sashen da na'urar ta duba",
    },
    "prediction": {
        "en": "Prediction",
        "ha": "Sakamako",
    },
    "confidence": {
        "en": "Confidence",
        "ha": "Tabbaci",
    },
    "low_confidence": {
        "en": (
            "Low confidence. Retake a sharper, closer photo of a single leaf "
            "under even lighting."
        ),
        "ha": (
            "Tabbaci ya yi ƙasa. Sake ɗaukar hoto mai haske, a kusa, na ganye ɗaya "
            "a cikin haske daidai."
        ),
    },
    "top3": {
        "en": "Top 3 classes",
        "ha": "Manyan zaɓuɓɓuka uku",
    },
    "advisory": {
        "en": "Field advisory",
        "ha": "Shawarar gona",
    },
    "advisory_tentative": {
        "en": "Treat this advisory as tentative until you confirm the symptoms on the plant.",
        "ha": (
            "Ka ɗauki wannan shawara a matsayin na wucin gadi har sai ka tabbatar da "
            "alamun a jikin shuka."
        ),
    },
    "causal_agent": {
        "en": "Causal agent",
        "ha": "Mai haddasa cuta",
    },
    "traits": {
        "en": "Observable traits",
        "ha": "Alamomin da ake gani",
    },
    "prevention": {
        "en": "Prevention and management",
        "ha": "Rigakafi da kulawa",
    },
    "disclaimer": {
        "en": (
            "This is field decision support, not a laboratory diagnosis. "
            "Follow local extension advice for pesticide choice and rates."
        ),
        "ha": (
            "Wannan taimako ne na yanke shawara a gona, ba gwajin ɗakin gwaje-gwaje ba. "
            "Bi shawarar jami'an gona na yankinku game da zaɓin magani da yawansa."
        ),
    },
    "model_caption": {
        "en": "Model: {architecture} · square crop {size}×{size}",
        "ha": "Na'ura: {architecture} · yanki murabba'i {size}×{size}",
    },
    "translation_note": {
        "en": "",
        "ha": "Fassarar Hausa — a tabbatar da kalmomin fasaha tare da jami'in gona.",
    },
    "read_aloud": {
        "en": "Read aloud",
        "ha": "Karanta da murya",
    },
    "preparing_audio": {
        "en": "Preparing audio...",
        "ha": "Ana shirya murya...",
    },
    "speech_offline": {
        "en": "Voice features need an internet connection. Scanning still works offline.",
        "ha": "Abubuwan murya suna buƙatar intanet. Duba cuta yana aiki ba tare da intanet ba.",
    },
    "voice_title": {
        "en": "Voice commands",
        "ha": "Umarnin murya",
    },
    "voice_help": {
        "en": 'Record and say "scan", "Hausa", "English", or "read aloud".',
        "ha": 'Naɗi muryarka ka faɗi "duba", "Hausa", "Turanci", ko "karanta".',
    },
    "voice_listening": {
        "en": "Listening to your command...",
        "ha": "Ana sauraron umarninka...",
    },
    "voice_heard": {
        "en": 'Heard: "{text}"',
        "ha": 'An ji: "{text}"',
    },
    "voice_unknown": {
        "en": 'Command not recognised. Say "scan", "Hausa", "English", or "read aloud".',
        "ha": 'Ba a gane umarnin ba. Faɗi "duba", "Hausa", "Turanci", ko "karanta".',
    },
    "voice_silent": {
        "en": "No speech was detected. Speak clearly and try again.",
        "ha": "Ba a ji magana ba. Yi magana a fili ka sake gwadawa.",
    },
    "voice_need_image": {
        "en": "Upload a tomato leaf photo first, then say \"scan\".",
        "ha": "Fara ɗora hoton ganyen tumatir, sannan ka faɗi \"duba\".",
    },
    "speech_result": {
        "en": "Prediction: {name}. Confidence: {confidence} percent.",
        "ha": "Sakamako: {name}. Tabbaci: kashi {confidence} cikin ɗari.",
    },
    "speech_low_confidence": {
        "en": "Confidence is low, so confirm the symptoms on the plant.",
        "ha": "Tabbaci ya yi ƙasa, don haka ka tabbatar da alamun a jikin shuka.",
    },
}


def t(key: str, lang: str, **values) -> str:
    entry = STRINGS[key]
    text = entry.get(lang) or entry["en"]
    return text.format(**values) if values else text
