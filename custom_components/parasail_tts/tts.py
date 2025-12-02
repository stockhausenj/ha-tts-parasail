"""Support for Parasail text-to-speech service."""
from __future__ import annotations

import base64
import json
import logging
from typing import Any

from homeassistant.components.tts import TextToSpeechEntity, TtsAudioType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_EXAGGERATION,
    CONF_MODEL,
    CONF_TEMPERATURE,
    CONF_VOICE,
    DEFAULT_CFG_WEIGHT,
    DEFAULT_EXAGGERATION,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_VOICE,
    DOMAIN,
    PARASAIL_API_URL,
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
        voice = config.get(CONF_VOICE, DEFAULT_VOICE)
        temperature = config.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)
        exaggeration = config.get(CONF_EXAGGERATION, DEFAULT_EXAGGERATION)

        _LOGGER.debug(
            "Requesting TTS: voice=%s, message_length=%d, temperature=%s, exaggeration=%s, cfg_weight=%s",
            voice,
            len(message),
            temperature,
            exaggeration,
            DEFAULT_CFG_WEIGHT
        )

        # Prepare request payload
        payload = {
            "temperature": temperature,
            "text": message,
            "voice": voice,
            "exaggeration": exaggeration,
            "cfg_weight": DEFAULT_CFG_WEIGHT,
        }

        try:
            session = async_get_clientsession(self.hass)
            headers = {
                "Content-Type": "application/json",
            }

            async with session.post(
                PARASAIL_API_URL,
                json=payload,
                headers=headers,
                timeout=30,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    _LOGGER.error(
                        "API request failed with status %d: %s",
                        response.status,
                        error_text
                    )
                    return None

                # Parse Server-Sent Events (SSE) streaming response
                audio_chunks = []
                chunk_count = 0

                async for line in response.content:
                    line_text = line.decode('utf-8').strip()

                    # SSE events are prefixed with "data: "
                    if line_text.startswith('data: '):
                        json_data = line_text[6:]  # Remove "data: " prefix

                        try:
                            event = json.loads(json_data)

                            # Process audio chunks
                            if event.get('type') == 'audio' and 'audio_content' in event:
                                # Decode base64 audio content
                                audio_chunk = base64.b64decode(event['audio_content'])
                                audio_chunks.append(audio_chunk)
                                chunk_count += 1
                                _LOGGER.debug(
                                    "Received audio chunk %d (%d bytes)",
                                    event.get('chunk', chunk_count),
                                    len(audio_chunk)
                                )

                            elif event.get('type') == 'error':
                                _LOGGER.error("API returned error event: %s", event)
                                return None

                        except json.JSONDecodeError as err:
                            _LOGGER.warning("Failed to parse SSE event JSON: %s", err)
                            continue

                # Concatenate all audio chunks
                if not audio_chunks:
                    _LOGGER.error("No audio chunks received from API")
                    return None

                audio_data = b''.join(audio_chunks)
                _LOGGER.info(
                    "Generated %d bytes of audio from %d chunks",
                    len(audio_data),
                    chunk_count
                )

            # Detect audio format from magic bytes
            if len(audio_data) >= 4:
                magic_bytes = audio_data[:4]
                _LOGGER.debug("Audio magic bytes: %s", magic_bytes.hex())

                # Check for WAV format (RIFF header)
                if magic_bytes == b'RIFF':
                    _LOGGER.info("Detected WAV format from API")
                    return ("wav", audio_data)

                # Check for MP3 format (ID3 tag or MPEG sync)
                elif magic_bytes[:3] == b'ID3' or (magic_bytes[0] == 0xFF and (magic_bytes[1] & 0xE0) == 0xE0):
                    _LOGGER.info("Detected MP3 format from API")
                    return ("mp3", audio_data)

                # Unknown format, log warning and assume WAV (since API returns WAV)
                else:
                    _LOGGER.warning(
                        "Unknown audio format, magic bytes: %s. Assuming WAV.",
                        magic_bytes.hex()
                    )
                    return ("wav", audio_data)

            # Fallback to WAV
            return ("wav", audio_data)
        except Exception as err:
            _LOGGER.error(
                "Error during TTS generation: %s (voice=%s, message_length=%d)",
                err,
                voice,
                len(message),
                exc_info=True
            )
            return None
