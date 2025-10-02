# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Sensor Platform for Home Assistant

Implements the sensor platform for monitoring EcoWater HydroLink devices.
This module defines all available sensors and their configurations based on
the actual device capabilities, using standardized imperial units.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Features:
- Comprehensive monitoring of EcoWater water softener systems
- Standardized imperial units (gallons, GPM, pounds, grains)
- Real-time water usage and flow monitoring
- Salt level and usage tracking
- System performance metrics
- Alert and maintenance status
- Device health and connectivity monitoring

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release with basic sensor support
  
- 0.2.0 (2025-10-02)
  * Added comprehensive sensor categories
  * Standardized on imperial units
  * Improved entity categorization
  
- 0.3.0 (2025-10-02)
  * Updated sensor list based on actual device capabilities
  * Removed unsupported sensors
  * Added all available device metrics
  * Improved documentation and organization

License: MIT
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
    "ALERTS": "System alerts and warnings",
    "SYSTEM": "System status and configuration"
}

# Set of sensors to be enabled by default
DEFAULT_ENABLED_SENSORS = {
    # Basic Status and System Information
    "_internal_is_online",              # Device online status
    "app_active",                       # Application active status
    "current_time_secs",                # Current device time
    "model_description",                # Model description (EWS ERRC3702R50)
    "nickname",                         # Device nickname
    
    # Water Usage and Flow Metrics (Imperial)
    "current_water_flow_gpm",           # Current water flow in GPM
    "gallons_used_today",              # Water used today in gallons
    "avg_daily_use_gals",              # Average daily usage in gallons
    "total_outlet_water_gals",         # Total treated water in gallons
    "peak_water_flow_gpm",             # Peak water flow in GPM
    "treated_water_avail_gals",        # Available treated water in gallons
    
    # Salt Management
    "salt_level_tenths",               # Current salt level in tenths
    "out_of_salt_estimate_days",       # Days until salt needed
    "avg_salt_per_regen_lbs",          # Average salt per regeneration (lbs)
    "total_salt_use_lbs",              # Total salt used (lbs)
    
    # System Performance
    "capacity_remaining_percent",       # Remaining capacity percentage
    "operating_capacity_grains",        # Operating capacity in grains
    "hardness_grains",                 # Water hardness in grains
    "rock_removed_since_rech_lbs",     # Hardness removed since recharge (lbs)
    "daily_avg_rock_removed_lbs",      # Daily average hardness removed (lbs)
    "total_rock_removed_lbs",          # Total hardness removed (lbs)
    
    # Regeneration Status
    "regen_status_enum",               # Current regeneration status
    "days_since_last_regen",           # Days since last regeneration
    "total_regens",                    # Total regeneration count
    "manual_regens",                   # Manual regeneration count
    "regen_time_rem_secs",             # Remaining regeneration time
    
    # Critical Alerts
    "low_salt_alert",                  # Low salt warning
    "error_code_alert",                # System error alert
    "flow_monitor_alert",              # Flow monitoring alert
    "excessive_water_use_alert",       # High water usage alert
    "floor_leak_detector_alert",       # Leak detection alert
    "service_reminder_alert",          # Service reminder alert
    
    # Signal and Connection
    "rf_signal_strength_dbm",          # WiFi signal strength
    "rf_signal_bars",                  # WiFi signal quality
    
    # System Stats
    "days_in_operation",               # Total days system has been running
    "power_outage_count",              # Number of power outages
    "service_reminder_months"          # Months until service needed
    "service_reminder_alert",      # Service needed reminder
    "flow_monitor_alert",         # Abnormal flow alert
    "excessive_water_use_alert",  # High water usage alert
    
    # Maintenance Info
    "service_reminder_months",    # Months until service needed
    "days_in_operation",         # Total days system has operated
}

# Descriptions for each sensor
SENSOR_DESCRIPTIONS = {
    # BASIC SYSTEM INFORMATION
    "_internal_is_online": {
        "name": "Online Status",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:wifi",
        "category": "BASIC",
    },
    "system_error": {
        "name": "System Error",
        "unit": None,
        "device_class": None,  # Removed PROBLEM as it's no longer a valid device class
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
    
        # BASIC SYSTEM INFORMATION
    "_internal_is_online": {
        "name": "Online Status",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:wifi-check",
        "category": "BASIC",
    },
    # BASIC SYSTEM INFO
    "app_active": {
        "name": "App Active",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:checkbox-marked-circle",
        "category": "BASIC",
    },
    "current_time_secs": {
        "name": "Device Time",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:clock-outline",
        "category": "BASIC",
    },
    "model_description": {
        "name": "Model",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:water-well",
        "category": "BASIC",
    },
    "nickname": {
        "name": "Device Name",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:label-outline",
        "category": "BASIC",
    },

    # WATER METRICS
    "current_water_flow_gpm": {
        "name": "Current Water Flow",
        "unit": "gpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-outline",
        "category": "WATER",
    },
    "gallons_used_today": {
        "name": "Water Used Today",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:water",
        "category": "WATER",
    },
    "avg_daily_use_gals": {
        "name": "Average Daily Water Usage",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:chart-timeline-variant",
        "category": "WATER",
    },
    "total_outlet_water_gals": {
        "name": "Total Treated Water",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:meter-water",
        "category": "WATER",
    },
    "peak_water_flow_gpm": {
        "name": "Peak Water Flow",
        "unit": "gpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:chart-bell-curve",
        "category": "WATER",
    },
    "treated_water_avail_gals": {
        "name": "Available Treated Water",
        "unit": UnitOfVolume.GALLONS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-check",
        "category": "WATER",
    },

    # SALT METRICS
    "salt_level_tenths": {
        "name": "Salt Level",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:salt",
        "category": "SALT",
    },
    "out_of_salt_estimate_days": {
        "name": "Days Until Salt Needed",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar-clock",
        "category": "SALT",
    },
    "avg_salt_per_regen_lbs": {
        "name": "Salt Used per Regeneration",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:scale-bathroom",
        "category": "SALT",
    },
    "total_salt_use_lbs": {
        "name": "Total Salt Used",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:scale",
        "category": "SALT",
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
    "operating_capacity_grains": {
        "name": "Operating Capacity",
        "unit": "grains",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water",
        "category": "PERFORMANCE",
    },
    "hardness_grains": {
        "name": "Water Hardness",
        "unit": "grains",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-outline",
        "category": "PERFORMANCE",
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
    "total_rock_removed_lbs": {
        "name": "Total Hardness Removed",
        "unit": UnitOfMass.POUNDS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:scale",
        "category": "PERFORMANCE",
    },

    # REGENERATION STATUS
    "regen_status_enum": {
        "name": "Regeneration Status",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:sync",
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
    },
    "manual_regens": {
        "name": "Manual Regenerations",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:refresh",
        "category": "REGEN",
    },
    "regen_time_rem_secs": {
        "name": "Regeneration Time Remaining",
        "unit": UnitOfTime.SECONDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer",
        "category": "REGEN",
    },
    
    # ALERTS
    "low_salt_alert": {
        "name": "Low Salt Alert",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:alert-circle",
        "category": "ALERTS",
    },
    "error_code_alert": {
        "name": "Error Code Alert",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:alert",
        "category": "ALERTS",
    },
    "flow_monitor_alert": {
        "name": "Flow Monitor Alert",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:water-alert",
        "category": "ALERTS",
    },
    "excessive_water_use_alert": {
        "name": "Excessive Water Use Alert",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:water-alert",
        "category": "ALERTS",
    },
    "floor_leak_detector_alert": {
        "name": "Leak Detector Alert",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:water-alert",
        "category": "ALERTS",
    },
    "service_reminder_alert": {
        "name": "Service Reminder Alert",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:tools",
        "category": "ALERTS",
    },

    # SYSTEM STATUS
    "rf_signal_strength_dbm": {
        "name": "WiFi Signal Strength",
        "unit": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi",
        "category": "SYSTEM",
    },
    "rf_signal_bars": {
        "name": "WiFi Signal Quality",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi",
        "category": "SYSTEM",
    },
    "days_in_operation": {
        "name": "Days in Operation",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:calendar",
        "category": "SYSTEM",
    },
    "power_outage_count": {
        "name": "Power Outage Count",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:power-plug-off",
        "category": "SYSTEM",
    },
    "service_reminder_months": {
        "name": "Months Until Service",
        "unit": UnitOfTime.MONTHS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:tools",
        "category": "SYSTEM",
    }
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
