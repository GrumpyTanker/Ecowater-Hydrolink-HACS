# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Data Update Coordinator

Handles data updates and synchronization between the HydroLink API
and Home Assistant entities. Manages the update schedule and provides
real-time updates through WebSocket connections.

Author: GrumpyTanker
Created: June 12, 2025
Updated: October 3, 2025
Version: 1.1.0

Changelog:
- 1.1.0 (2025-10-03)
  * Enhanced test coverage with comprehensive coordinator testing
  * Improved error handling for authentication and connection failures
  * Better data validation and empty response handling
  * Updated for Home Assistant 2024.10.0+ and Python 3.12+

- 1.0.0 (2025-10-02)
  * Initial HACS-compatible release
  * Added WebSocket support for real-time updates
  * Improved error handling and logging
  * Added type hints and better documentation

- 0.1.0 (2025-06-12)
  * Initial release
  * Basic data update coordination
  * Polling implementation

License: MIT
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
    """Data update coordinator for HydroLink water softener devices.
    
    This coordinator manages the periodic fetching of data from the HydroLink API
    and provides a unified interface for Home Assistant entities to access device
    information. It handles authentication, error recovery, and data synchronization.
    
    The coordinator updates data every 30 seconds and uses the HydroLink API's
    WebSocket functionality to ensure fresh, real-time data rather than cached values.
    
    Key Features:
        - Automatic data refresh every 30 seconds
        - Real-time updates via WebSocket connections
        - Robust error handling and recovery
        - Authentication management and renewal
        - Multi-device support
        
    Attributes:
        api: HydroLinkApi instance for communicating with the service
        hass: Home Assistant instance
        config_entry: Configuration entry containing user credentials
        
    Example:
        coordinator = HydroLinkDataUpdateCoordinator(hass, config_entry)
        await coordinator.async_config_entry_first_refresh()
        device_data = coordinator.data
    """

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
