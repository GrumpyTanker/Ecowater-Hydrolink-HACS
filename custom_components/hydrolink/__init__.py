# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Home Assistant Integration

Main module for the Home Assistant integration with EcoWater HydroLink.
Handles component setup, config flow, and service registration.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic integration setup
  * Config flow implementation
  
- 0.2.0 (2025-10-02)
  * Added service registration
  * Improved error handling
  * Added type hints
  * Added data update coordinator

License: MIT
See LICENSE file in the project root for full license information.
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import DOMAIN
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
