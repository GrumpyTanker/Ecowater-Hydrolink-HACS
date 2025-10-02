# -*- coding: utf-8 -*-
"""
The HydroLink integration.

Copyright 2025 GrumpyTanker

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUTHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import HydroLinkDataUpdateCoordinator


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
