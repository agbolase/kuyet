"""Online voice features: read results aloud and understand spoken commands.

Both directions use Google's public speech services, so they need internet.
Disease scanning itself stays fully offline.
"""

from __future__ import annotations

import re
import unicodedata
from io import BytesIO

TTS_LANG = {"en": "en", "ha": "ha"}
STT_LANG = {"en": "en-NG", "ha": "ha-NG"}

# Checked in order: "translate to English" must resolve to English, not Hausa.
COMMAND_WORDS = (
    ("english", ("english", "turanci", "ingilishi", "inglishi")),
    ("hausa", ("hausa", "fassara", "translate", "translation")),
    ("read", ("read", "speak", "aloud", "karanta", "saurara", "fada", "faɗa")),
    ("scan", ("scan", "predict", "check", "detect", "duba", "bincika", "gwada")),
)

_HOOKED = str.maketrans({"ɓ": "b", "ɗ": "d", "ƙ": "k", "ƴ": "y", "Ɓ": "b", "Ɗ": "d", "Ƙ": "k", "Ƴ": "y"})


class SpeechUnavailable(RuntimeError):
    """Raised when Google speech services cannot be reached."""


def _normalize(text: str) -> str:
    text = text.translate(_HOOKED).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9' ]+", " ", text)


def parse_command(text: str) -> str | None:
    words = set(_normalize(text).split())
    for command, keywords in COMMAND_WORDS:
        if any(_normalize(keyword).strip() in words for keyword in keywords):
            return command
    return None


def spoken_form(text: str, lang: str) -> str:
    """Drop bracketed glosses and symbols that sound odd when read."""
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = text.replace("–", " zuwa " if lang == "ha" else " to ")
    text = text.replace("“", "").replace("”", "")
    return re.sub(r"\s+", " ", text).strip()


def synthesize(text: str, lang: str) -> bytes:
    from gtts import gTTS
    from gtts.tts import gTTSError

    buffer = BytesIO()
    try:
        gTTS(text=text, lang=TTS_LANG.get(lang, "en")).write_to_fp(buffer)
    except (gTTSError, OSError) as error:
        raise SpeechUnavailable(str(error)) from error
    return buffer.getvalue()


def transcribe_command(wav_bytes: bytes, lang: str) -> tuple[str, str | None]:
    """Return (transcript, command). Tries the UI language first, then the other."""
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(BytesIO(wav_bytes)) as source:
        audio = recognizer.record(source)

    order = [lang] + [code for code in STT_LANG if code != lang]
    transcript = ""
    for code in order:
        try:
            heard = recognizer.recognize_google(audio, language=STT_LANG[code])
        except sr.UnknownValueError:
            continue
        except sr.RequestError as error:
            raise SpeechUnavailable(str(error)) from error
        transcript = transcript or heard
        command = parse_command(heard)
        if command:
            return heard, command
    return transcript, None
