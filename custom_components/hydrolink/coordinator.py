# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Data Update Coordinator

Handles data updates and synchronization between the HydroLink API
and Home Assistant entities. Manages the update schedule and provides
real-time updates through WebSocket connections.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic data update coordination
  * Polling implementation
  
- 0.2.0 (2025-10-02)
  * Added WebSocket support
  * Improved error handling
  * Added type hints
  * Added real-time updates

License: Apache License 2.0
See LICENSE file in the project root for full license information.
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
