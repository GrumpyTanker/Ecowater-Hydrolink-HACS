# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Home Assistant Integration

Main module for the Home Assistant integration with EcoWater HydroLink.
Handles component setup, config flow, and service registration.

Author: GrumpyTanker
Created: June 12, 2025
Updated: October 3, 2025
Version: 1.1.0

Changelog:
- 1.1.0 (2025-10-03)
  * Enhanced test coverage to 58% (55+ comprehensive tests)
  * Fixed HACS validation issues and CI/CD pipeline
  * Improved error handling and WebSocket stability
  * Updated for Home Assistant 2024.10.0+ and Python 3.12+
  * Repository cleanup and documentation improvements

- 1.0.0 (2025-10-02)
  * Initial HACS-compatible release
  * Complete restructure for HACS compliance
  * Added comprehensive testing setup
  * Updated to MIT license
  * Improved documentation and translations

- 0.2.0 (2025-06-12)
  * Added service registration
  * Improved error handling
  * Added type hints
  * Added data update coordinator

- 0.1.0 (2025-06-12)
  * Initial release
  * Basic integration setup
  * Config flow implementation

License: MIT
See LICENSE file in the project root for full license information.
"""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

# Since we use config flow, this is an empty schema
CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)
from .coordinator import HydroLinkDataUpdateCoordinator
from .services import async_setup_services

PLATFORMS = [Platform.SENSOR]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HydroLink component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HydroLink from a config entry.

    This function is called when a config entry is created for the integration.
    It initializes the data coordinator and forwards the setup to the sensor
    platform.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns:
        True if the setup was successful.
    """
    # Ensure the domain data is initialized
    hass.data.setdefault(DOMAIN, {})

    # Create and initialize the data update coordinator
    coordinator = HydroLinkDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator in the hass data
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Set up services
    await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.

    This function is called when a config entry is removed. It unloads the
    sensor platform and removes the coordinator from the hass data.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns:
        True if the unload was successful.
    """
    # Unload the platforms associated with the config entry
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # Remove the coordinator from the hass data
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
