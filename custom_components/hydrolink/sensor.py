# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Sensor Platform for Home Assistant

Implements the sensor platform for monitoring EcoWater HydroLink devices.
This module defines all available sensors and their configurations including
units, device classes, and state classes.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic sensor definitions
  * Default enabled sensors
  
- 0.2.0 (2025-10-02)
  * Added comprehensive sensor categories
  * Expanded sensor definitions
  * Added proper unit conversions
  * Improved entity categorization

License: Apache License 2.0
See LICENSE file in the project root for full license information.
"""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfVolume,
    UnitOfTime,
    UnitOfMass,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN

# All available sensor categories
SENSOR_CATEGORIES = {
    "BASIC": "Basic system information",
    "WATER": "Water usage and flow metrics",
    "SALT": "Salt level and usage metrics",
    "REGEN": "Regeneration information",
    "PERFORMANCE": "System performance metrics",
    "MAINTENANCE": "Maintenance and service information",
    "ADVANCED": "Advanced technical metrics",
    "ALERTS": "System alerts and warnings",
    "HARDWARE": "Hardware and device information"
}

# Set of sensors to be enabled by default
DEFAULT_ENABLED_SENSORS = {
    # Basic status
    "online",
    "system_error",
    "vacation_mode",
    
    # Critical metrics
    "water_flow_rate",
    "salt_level_percent",
    "salt_level_days_remaining",
    "out_of_salt_date",
    "capacity_remaining_percent",
    
    # Water usage
    "water_usage_today",
    "water_usage_daily_average",
    "water_usage_yesterday",
    "water_hardness",
    
    # Regeneration
    "regeneration_days_remaining",
    "regeneration_last",
    "days_since_last_regen",
    
    # Environmental
    "water_pressure",
    "inlet_water_pressure",
    "outlet_water_pressure",
    "water_temperature",
    "inlet_water_temperature",
    "outlet_water_temperature",
    
    # Alerts
    "low_salt_alert",
    "error_code_alert",
    "service_reminder_alert",
}

# Descriptions for each sensor
SENSOR_DESCRIPTIONS = {
    # BASIC SYSTEM INFORMATION
    "online": {
        "name": "Online Status",
        "unit": None,
        "device_class": SensorDeviceClass.CONNECTIVITY,
        "state_class": None,
        "icon": "mdi:wifi",
        "category": "BASIC",
    },
    "system_error": {
        "name": "System Error",
        "unit": None,
        "device_class": SensorDeviceClass.PROBLEM,
        "state_class": None,
        "icon": "mdi:alert",
        "category": "BASIC",
    },
    "vacation_mode": {
        "name": "Vacation Mode",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:airplane",
        "category": "BASIC",
    },
    
    # WATER METRICS
    "water_flow_rate": {
        "name": "Current Water Flow",
        "unit": "gpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-pump",
        "category": "WATER",
    },
    "peak_water_flow_gpm": {
        "name": "Peak Water Flow",
        "unit": "gpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-pump-outline",
        "category": "WATER",
    },
    "water_usage_today": {
        "name": "Water Usage Today",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:water",
        "category": "WATER",
    },
    "water_usage_daily_average": {
        "name": "Average Daily Water Usage",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:water",
        "category": "WATER",
    },
    "total_outlet_water_gals": {
        "name": "Total Treated Water",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:water-check",
        "category": "WATER",
    },
    "treated_water_avail_gals": {
        "name": "Available Treated Water",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-check-outline",
        "category": "WATER",
    },

    # SALT METRICS
    "salt_level_percent": {
        "name": "Salt Level",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:salt",
        "category": "SALT",
    },
    "salt_level_days_remaining": {
        "name": "Salt Days Remaining",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar-clock",
        "category": "SALT",
    },
    "out_of_salt_date": {
        "name": "Out of Salt Date",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:calendar-alert",
        "category": "SALT",
    },
    "total_salt_use_lbs": {
        "name": "Total Salt Used",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:scale",
        "category": "SALT",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "avg_salt_per_regen_lbs": {
        "name": "Average Salt per Regeneration",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:scale-bathroom",
        "category": "SALT",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    
    # REGENERATION METRICS
    "regeneration_days_remaining": {
        "name": "Days Until Regeneration",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar-clock",
        "category": "REGEN",
    },
    "regeneration_last": {
        "name": "Last Regeneration",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:calendar-clock",
        "category": "REGEN",
    },
    "days_since_last_regen": {
        "name": "Days Since Last Regeneration",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar-clock",
        "category": "REGEN",
    },
    "total_regens": {
        "name": "Total Regenerations",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:refresh",
        "category": "REGEN",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "avg_days_between_regens": {
        "name": "Average Days Between Regenerations",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar-refresh",
        "category": "REGEN",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    
    # PERFORMANCE METRICS
    "capacity_remaining_percent": {
        "name": "Capacity Remaining",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-percent",
        "category": "PERFORMANCE",
    },
    "water_hardness": {
        "name": "Water Hardness",
        "unit": "gpg",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-outline",
        "category": "PERFORMANCE",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "rock_removed_since_rech_lbs": {
        "name": "Hardness Removed Since Recharge",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:scale",
        "category": "PERFORMANCE",
    },
    "daily_avg_rock_removed_lbs": {
        "name": "Average Daily Hardness Removed",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:scale-bathroom",
        "category": "PERFORMANCE",
    },

    # PRESSURE AND TEMPERATURE
    "water_pressure": {
        "name": "Water Pressure",
        "unit": UnitOfPressure.PSI,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:gauge",
        "category": "PERFORMANCE",
    },
    "inlet_water_pressure": {
        "name": "Inlet Water Pressure",
        "unit": UnitOfPressure.PSI,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:gauge",
        "category": "PERFORMANCE",
    },
    "outlet_water_pressure": {
        "name": "Outlet Water Pressure",
        "unit": UnitOfPressure.PSI,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:gauge",
        "category": "PERFORMANCE",
    },
    "water_temperature": {
        "name": "Water Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "category": "PERFORMANCE",
    },
    "inlet_water_temperature": {
        "name": "Inlet Water Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "category": "PERFORMANCE",
    },
    "outlet_water_temperature": {
        "name": "Outlet Water Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "category": "PERFORMANCE",
    },
    
    # MAINTENANCE AND SERVICE
    "service_reminder_months": {
        "name": "Months Until Service",
        "unit": UnitOfTime.MONTHS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:tools",
        "category": "MAINTENANCE",
    },
    "days_in_operation": {
        "name": "Days in Operation",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:clock-outline",
        "category": "MAINTENANCE",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    
    # ALERTS AND WARNINGS
    "low_salt_alert": {
        "name": "Low Salt Alert",
        "unit": None,
        "device_class": SensorDeviceClass.PROBLEM,
        "state_class": None,
        "icon": "mdi:alert-circle",
        "category": "ALERTS",
    },
    "error_code_alert": {
        "name": "Error Code Alert",
        "unit": None,
        "device_class": SensorDeviceClass.PROBLEM,
        "state_class": None,
        "icon": "mdi:alert",
        "category": "ALERTS",
    },
    "service_reminder_alert": {
        "name": "Service Reminder",
        "unit": None,
        "device_class": SensorDeviceClass.PROBLEM,
        "state_class": None,
        "icon": "mdi:tools",
        "category": "ALERTS",
    },
    "flow_monitor_alert": {
        "name": "Flow Monitor Alert",
        "unit": None,
        "device_class": SensorDeviceClass.PROBLEM,
        "state_class": None,
        "icon": "mdi:water-alert",
        "category": "ALERTS",
    },
    "excessive_water_use_alert": {
        "name": "Excessive Water Use Alert",
        "unit": None,
        "device_class": SensorDeviceClass.PROBLEM,
        "state_class": None,
        "icon": "mdi:water-alert",
        "category": "ALERTS",
    },
    
    # HARDWARE AND CONNECTIVITY
    "rf_signal_strength_dbm": {
        "name": "WiFi Signal Strength",
        "unit": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi",
        "category": "HARDWARE",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "rf_signal_bars": {
        "name": "WiFi Signal Bars",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi",
        "category": "HARDWARE",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "power_outage_count": {
        "name": "Power Outage Count",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:power-plug-off",
        "category": "HARDWARE",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "water_hardness": {
        "name": "Water Hardness",
        "unit": "gpg",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-outline",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "water_usage_daily_average": {
        "name": "Average Daily Water Usage",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,  # WATER is no longer a valid device class
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:water",
    },
    "water_usage_today": {
        "name": "Water Usage Today",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,  # WATER is no longer a valid device class
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:water",
    },
    "water_usage_yesterday": {
        "name": "Water Usage Yesterday",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,  # WATER is no longer a valid device class
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:water",
    },
    "online": {
        "name": "Online Status",
        "unit": None,
        "device_class": None,  # CONNECTIVITY is not available in current HA version
        "state_class": None,
        "icon": "mdi:wifi",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "out_of_salt_date": {
        "name": "Out of Salt Since",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:calendar-alert",
    },
    "salt_level_percent": {
        "name": "Salt Level",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:grain",
    },
    "salt_level_days_remaining": {
        "name": "Salt Days Remaining",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar-end",
    },
    "system_error": {
        "name": "System Error",
        "unit": None,
        "device_class": None,  # PROBLEM is no longer a valid device class
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "vacation_mode": {
        "name": "Vacation Mode",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:beach",
    },
    "water_pressure": {
        "name": "Water Pressure",
        "unit": UnitOfPressure.PSI,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:gauge",
    },
    "inlet_water_pressure": {
        "name": "Inlet Water Pressure",
        "unit": UnitOfPressure.PSI,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:gauge",
    },
    "outlet_water_pressure": {
        "name": "Outlet Water Pressure",
        "unit": UnitOfPressure.PSI,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:gauge",
    },
    "water_temperature": {
        "name": "Water Temperature",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "inlet_water_temperature": {
        "name": "Inlet Water Temperature",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "outlet_water_temperature": {
        "name": "Outlet Water Temperature",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the HydroLink sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for device in coordinator.data:
        # Assuming 'demand_softener' is the target device type
        if device.get("system_type") != "demand_softener":
            continue
        
        device_name = device.get("nickname", "EcoWater Softener")
        
        for prop_name, prop_info in device.get("properties", {}).items():
            if isinstance(prop_info, dict) and "value" in prop_info:
                entities.append(HydroLinkSensor(coordinator, device["id"], prop_name, device_name))

    async_add_entities(entities)


class HydroLinkSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HydroLink sensor."""

    def __init__(self, coordinator, device_id, property_name, device_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._property_name = property_name
        self._device_name = device_name

        description = SENSOR_DESCRIPTIONS.get(property_name)
        if description:
            self._attr_name = f"{device_name} {description['name']}"
            self._attr_native_unit_of_measurement = description.get("unit")
            self._attr_device_class = description.get("device_class")
            self._attr_state_class = description.get("state_class")
            self._attr_icon = description.get("icon")
            self._attr_entity_category = description.get("entity_category")
        else:
            self._attr_name = f"{device_name} {property_name.replace('_', ' ').title()}"

        self._attr_unique_id = f"hydrolink_{device_id}_{property_name}"
        
        # Set whether the entity should be enabled by default
        self._attr_entity_registry_enabled_default = (
            self._property_name in DEFAULT_ENABLED_SENSORS
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for device in self.coordinator.data:
            if device["id"] == self._device_id:
                value = device["properties"][self._property_name].get("value")
                
                # Handle numeric sensors when value is unknown
                if (value == "unknown" and self.device_class in [
                    SensorDeviceClass.ENERGY,
                    SensorDeviceClass.POWER,
                    SensorDeviceClass.CURRENT,
                    SensorDeviceClass.VOLTAGE,
                    SensorDeviceClass.PRESSURE,
                    SensorDeviceClass.TEMPERATURE
                ]):
                    return None
                    
                return value
        return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "EcoWater",
        }
