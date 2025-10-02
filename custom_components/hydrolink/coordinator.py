# -*- coding: utf-8 -*-
"""
Data update coordinator for the HydroLink integration.

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
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .api import HydroLinkApi, CannotConnect, InvalidAuth
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HydroLinkDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HydroLink data from the API."""

    def __init__(self, hass: HomeAssistant, entry):
        """Initialize the data update coordinator.

        Args:
            hass: The Home Assistant instance.
            entry: The config entry for this integration.
        """
        self.api = HydroLinkApi(
            entry.data[CONF_EMAIL],
            entry.data[CONF_PASSWORD],
        )
        # Initialize the DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Fetch data from the API endpoint.

        This method is called by the DataUpdateCoordinator to refresh the data.
        It calls the API to get the latest device data and handles potential
        connection or authentication errors.

        Returns:
            The latest data from the API.

        Raises:
            UpdateFailed: If the API call fails due to authentication or
                connection issues.
        """
        try:
            # Fetch the data from the API
            return await self.hass.async_add_executor_job(self.api.get_data)
        except InvalidAuth as err:
            raise UpdateFailed("Invalid authentication") from err
        except CannotConnect as err:
            raise UpdateFailed("Error communicating with API") from err
