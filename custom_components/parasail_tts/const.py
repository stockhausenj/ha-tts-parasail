"""Constants for the Parasail TTS integration."""

DOMAIN = "parasail_tts"

CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_VOICE = "voice"

DEFAULT_MODEL = "parasail-resemble-tts-en"
DEFAULT_VOICE = "oai_nova"
DEFAULT_TEMPERATURE = 0.1

PARASAIL_API_BASE = "https://api.parasail.io/v1"

# Available TTS models on Parasail
PARASAIL_TTS_MODELS = [
    "parasail-resemble-tts-en",
]

# Available voices for TTS
PARASAIL_TTS_VOICES = [
    "oai_ash",
    "oai_coral",
    "oai_echo",
    "oai_fable",
    "oai_nova",
    "oai_onyx",
    "oai_sage",
    "oai_shimmer",
]

# Voice name mapping for display purposes
VOICE_NAMES = {
    "oai_ash": "Ash",
    "oai_coral": "Coral",
    "oai_echo": "Echo",
    "oai_fable": "Fable",
    "oai_nova": "Nova",
    "oai_onyx": "Onyx",
    "oai_sage": "Sage",
    "oai_shimmer": "Shimmer",
}
