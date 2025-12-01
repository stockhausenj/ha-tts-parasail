"""Constants for the Parasail TTS integration."""

DOMAIN = "parasail_tts"

CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_VOICE = "voice"

DEFAULT_MODEL = "parasail-resemble-tts-en"
DEFAULT_VOICE = "oai-sky"
DEFAULT_TEMPERATURE = 0.1

PARASAIL_API_BASE = "https://api.parasail.io/v1"

# Available TTS models on Parasail
PARASAIL_TTS_MODELS = [
    "parasail-resemble-tts-en",
]

# Available voices for TTS
PARASAIL_TTS_VOICES = [
    "oai-sky",
]

# Voice name mapping for display purposes
VOICE_NAMES = {
    "oai-sky": "Sky",
}
