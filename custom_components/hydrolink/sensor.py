"""
Sensor platform for the HydroLink integration.

Author: GrumpyTanker + AI
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
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN

# Set of sensors to be enabled by default
DEFAULT_ENABLED_SENSORS = {
    "regeneration_days_remaining",
    "regeneration_last",
    "water_flow_rate",
    "water_hardness",
    "water_usage_daily_average",
    "water_usage_today",
    "water_usage_yesterday",
    "online",
    "out_of_salt_date",
    "salt_level_percent",
    "salt_level_days_remaining",
    "system_error",
    "vacation_mode",
    "water_pressure",
    "inlet_water_pressure",
    "outlet_water_pressure",
    "water_temperature",
    "inlet_water_temperature",
    "outlet_water_temperature",
}

# Descriptions for each sensor
SENSOR_DESCRIPTIONS = {
    "regeneration_days_remaining": {
        "name": "Regeneration Days Remaining",
        "unit": UnitOfTime.DAYS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:counter",
    },
    "regeneration_last": {
        "name": "Last Regeneration",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:calendar-clock",
    },
    "water_flow_rate": {
        "name": "Water Flow Rate",
        "unit": "gpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-pump",
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
        "device_class": SensorDeviceClass.WATER,
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:water",
    },
    "water_usage_today": {
        "name": "Water Usage Today",
        "unit": UnitOfVolume.GALLONS,
        "device_class": SensorDeviceClass.WATER,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:water",
    },
    "water_usage_yesterday": {
        "name": "Water Usage Yesterday",
        "unit": UnitOfVolume.GALLONS,
        "device_class": SensorDeviceClass.WATER,
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:water",
    },
    "online": {
        "name": "Online Status",
        "unit": None,
        "device_class": SensorDeviceClass.CONNECTIVITY,
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
        "device_class": SensorDeviceClass.PROBLEM,
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
                return device["properties"][self._property_name].get("value")
        return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "EcoWater",
        }
