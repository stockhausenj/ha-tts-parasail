"""Support for Parasail text-to-speech service."""
from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

from homeassistant.components.tts import TextToSpeechEntity, TtsAudioType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_API_KEY,
    CONF_MODEL,
    CONF_VOICE,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_VOICE,
    DOMAIN,
    PARASAIL_API_BASE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Parasail TTS platform."""
    async_add_entities([ParasailTTSEntity(config_entry)])


class ParasailTTSEntity(TextToSpeechEntity):
    """Parasail text-to-speech entity."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize Parasail TTS entity."""
        self._config_entry = config_entry
        self._attr_name = f"Parasail TTS {config_entry.data.get(CONF_MODEL, DEFAULT_MODEL)}"
        self._attr_unique_id = config_entry.entry_id

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        # Parasail TTS models support English
        # Add more languages as they become available
        return ["en"]

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return "en"

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        return []

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> TtsAudioType:
        """Load TTS audio from Parasail API."""
        _LOGGER.debug("Generating TTS audio for message: %s (language: %s)", message, language)

        # Get configuration
        config = self._config_entry.options or self._config_entry.data
        api_key = self._config_entry.data[CONF_API_KEY]
        model = config.get(CONF_MODEL, DEFAULT_MODEL)
        voice = config.get(CONF_VOICE, DEFAULT_VOICE)

        def _generate_speech():
            """Generate speech in executor."""
            client = OpenAI(
                base_url=PARASAIL_API_BASE,
                api_key=api_key,
            )

            _LOGGER.debug(
                "Requesting TTS: model=%s, voice=%s, message_length=%d",
                model,
                voice,
                len(message)
            )

            # Use the audio.speech.create endpoint for TTS
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=message,
                extra_body={"temperature": DEFAULT_TEMPERATURE},
            )

            # The response is a streaming response, read the content
            return response.content

        try:
            audio_data = await self.hass.async_add_executor_job(_generate_speech)
            _LOGGER.debug("Generated %d bytes of audio", len(audio_data))

            # Return the audio data as MP3 format
            return ("mp3", audio_data)
        except Exception as err:
            _LOGGER.error(
                "Error during TTS generation: %s (model=%s, message_length=%d)",
                err,
                model,
                len(message),
                exc_info=True
            )
            return None
