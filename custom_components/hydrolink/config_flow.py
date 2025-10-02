# -*- coding: utf-8 -*-
"""
Config flow for HydroLink integration.

Copyright 2025 GrumpyTanker

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .api import HydroLinkApi, CannotConnect, InvalidAuth

_LOGGER = logging.getLogger(__name__)

# Schema for the user input form
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HydroLink."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the user configuration.

        This is called when a user initiates a new configuration flow. It
        presents a form for the user to enter their credentials, validates
        them, and creates a config entry on success.

        Args:
            user_input: The user-provided input from the form.

        Returns:
            A form to be shown to the user, or a result indicating success
            or failure.
        """
        errors = {}
        if user_input is not None:
            try:
                # Create an API instance and attempt to log in
                api = HydroLinkApi(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])
                await self.hass.async_add_executor_job(api.login)
                
                # Set the unique ID for the config entry and check for duplicates
                await self.async_set_unique_id(user_input[CONF_EMAIL])
                self._abort_if_unique_id_configured()

                # Create the config entry
                return self.async_create_entry(title=user_input[CONF_EMAIL], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # Display the form with any errors
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
