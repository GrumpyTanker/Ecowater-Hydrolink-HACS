"""Unit tests for the HydroLink sensor platform."""
from unittest.mock import Mock, patch
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfVolume,
    UnitOfTime,
)
from custom_components.hydrolink.sensor import (
    HydroLinkSensor,
    async_setup_entry,
    DEFAULT_ENABLED_SENSORS,
    SENSOR_DESCRIPTIONS,
)

# Test data
MOCK_DEVICE_ID = "test-device-id"
MOCK_DEVICE_NAME = "Test Device"
MOCK_PROPERTY = "water_usage_today"
MOCK_VALUE = 100

@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = Mock()
    coordinator.data = [
        {
            "id": MOCK_DEVICE_ID,
            "properties": {
                MOCK_PROPERTY: {"value": MOCK_VALUE}
            }
        }
    ]
    return coordinator

@pytest.fixture
def sensor(mock_coordinator):
    """Create a HydroLinkSensor instance for testing."""
    return HydroLinkSensor(
        mock_coordinator,
        MOCK_DEVICE_ID,
        MOCK_PROPERTY,
        MOCK_DEVICE_NAME
    )

def test_sensor_creation(sensor):
    """Test sensor object creation."""
    assert sensor._device_id == MOCK_DEVICE_ID
    assert sensor._property_name == MOCK_PROPERTY
    assert sensor._device_name == MOCK_DEVICE_NAME

def test_sensor_native_value(sensor):
    """Test sensor value retrieval."""
    assert sensor.native_value == MOCK_VALUE

def test_sensor_attributes(sensor):
    """Test sensor attributes from descriptions."""
    description = SENSOR_DESCRIPTIONS.get(MOCK_PROPERTY)
    if description:
        assert sensor._attr_native_unit_of_measurement == description.get("unit")
        assert sensor._attr_device_class == description.get("device_class")
        assert sensor._attr_state_class == description.get("state_class")
        assert sensor._attr_icon == description.get("icon")

def test_sensor_unique_id(sensor):
    """Test sensor unique ID generation."""
    assert sensor._attr_unique_id == f"hydrolink_{MOCK_DEVICE_ID}_{MOCK_PROPERTY}"

def test_sensor_device_info(sensor):
    """Test sensor device info."""
    device_info = sensor.device_info
    assert device_info["identifiers"] == {("hydrolink", MOCK_DEVICE_ID)}
    assert device_info["name"] == MOCK_DEVICE_NAME
    assert device_info["manufacturer"] == "EcoWater"

def test_sensor_default_enabled(sensor):
    """Test sensor default enabled state."""
    assert sensor._attr_entity_registry_enabled_default == (
        sensor._property_name in DEFAULT_ENABLED_SENSORS
    )

@pytest.mark.asyncio
async def test_async_setup_entry(hass: HomeAssistant):
    """Test platform setup."""
    mock_entry = Mock()
    mock_coordinator = Mock()
    mock_coordinator.data = [
        {
            "id": MOCK_DEVICE_ID,
            "system_type": "demand_softener",
            "nickname": MOCK_DEVICE_NAME,
            "properties": {
                "water_usage_today": {"value": 100},
                "salt_level": {"value": 50}
            }
        }
    ]
    
    # Set up the hass mock properly
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {"hydrolink": {mock_entry.entry_id: mock_coordinator}}
    
    # Create the async_add_entities mock
    async_add_entities = Mock()
    await async_setup_entry(hass, mock_entry, async_add_entities)
    
    # Verify entities were created and added
    assert async_add_entities.called
    entities = async_add_entities.call_args[0][0]
    assert len(entities) == 2  # Two properties in mock data