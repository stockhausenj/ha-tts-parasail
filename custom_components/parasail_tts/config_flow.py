"""Config flow for Parasail TTS integration."""
from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_API_KEY,
    CONF_MODEL,
    CONF_VOICE,
    DEFAULT_MODEL,
    DEFAULT_VOICE,
    DOMAIN,
    PARASAIL_API_BASE,
    PARASAIL_TTS_MODELS,
    PARASAIL_TTS_VOICES,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    def _test_connection():
        """Test connection to Parasail API."""
        client = OpenAI(
            base_url=PARASAIL_API_BASE,
            api_key=data[CONF_API_KEY],
        )

        # Test the API with a simple TTS request
        response = client.audio.speech.create(
            model=data.get(CONF_MODEL, DEFAULT_MODEL),
            voice=data.get(CONF_VOICE, DEFAULT_VOICE),
            input="Test",
        )

        return response.content

    try:
        # Test the API key with a simple TTS request
        await hass.async_add_executor_job(_test_connection)
    except Exception as err:
        _LOGGER.error("Failed to connect to Parasail API: %s", err)
        raise InvalidAuth from err

    return {"title": f"Parasail TTS ({data.get(CONF_MODEL, DEFAULT_MODEL)})"}


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
                        PARASAIL_TTS_VOICES
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
            ): vol.In(PARASAIL_TTS_VOICES),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
        )


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
