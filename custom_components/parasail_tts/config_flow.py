"""Config flow for Parasail TTS integration."""
from __future__ import annotations

import base64
import json
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_API_KEY,
    CONF_MODEL,
    CONF_VOICE,
    DEFAULT_CFG_WEIGHT,
    DEFAULT_EXAGGERATION,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_VOICE,
    DOMAIN,
    PARASAIL_API_URL,
    PARASAIL_TTS_MODELS,
    VOICE_NAMES,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Test the API with a simple TTS request
    session = async_get_clientsession(hass)

    payload = {
        "temperature": DEFAULT_TEMPERATURE,
        "text": "Test",
        "voice": data.get(CONF_VOICE, DEFAULT_VOICE),
        "exaggeration": DEFAULT_EXAGGERATION,
        "cfg_weight": DEFAULT_CFG_WEIGHT,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {data[CONF_API_KEY]}",
    }

    try:
        async with session.post(
            PARASAIL_API_URL,
            json=payload,
            headers=headers,
            timeout=10,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                _LOGGER.error("API validation failed: %s", error_text)
                raise InvalidAuth

            # Parse Server-Sent Events (SSE) streaming response to validate
            audio_received = False

            async for line in response.content:
                line_text = line.decode('utf-8').strip()

                # SSE events are prefixed with "data: "
                if line_text.startswith('data: '):
                    json_data = line_text[6:]  # Remove "data: " prefix

                    try:
                        event = json.loads(json_data)

                        # Check if we received valid audio data
                        if event.get('type') == 'audio' and 'audio_content' in event:
                            # Validate that audio_content is valid base64
                            base64.b64decode(event['audio_content'])
                            audio_received = True
                            # We only need to validate one chunk
                            break

                        elif event.get('type') == 'error':
                            _LOGGER.error("API returned error during validation: %s", event)
                            raise InvalidAuth

                    except (json.JSONDecodeError, base64.binascii.Error) as err:
                        _LOGGER.error("Failed to parse or decode API response: %s", err)
                        raise InvalidAuth from err

            if not audio_received:
                _LOGGER.error("No valid audio data received from API")
                raise InvalidAuth

    except InvalidAuth:
        raise
    except Exception as err:
        _LOGGER.error("Failed to connect to Parasail API: %s", err)
        raise InvalidAuth from err

    return {"title": f"Parasail TTS ({data.get(CONF_VOICE, DEFAULT_VOICE)})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Parasail TTS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_MODEL, default=DEFAULT_MODEL): vol.In(
                        PARASAIL_TTS_MODELS
                    ),
                    vol.Required(CONF_VOICE, default=DEFAULT_VOICE): vol.In(
                        VOICE_NAMES
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Parasail TTS."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        super().__init__()

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current options, fallback to data if options not set
        config_entry = self.config_entry
        options = config_entry.options or config_entry.data

        schema_dict = {
            vol.Required(
                CONF_MODEL,
                default=options.get(CONF_MODEL, DEFAULT_MODEL),
            ): vol.In(PARASAIL_TTS_MODELS),
            vol.Required(
                CONF_VOICE,
                default=options.get(CONF_VOICE, DEFAULT_VOICE),
            ): vol.In(VOICE_NAMES),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
        )


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
