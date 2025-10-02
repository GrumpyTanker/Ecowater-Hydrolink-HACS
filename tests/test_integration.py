"""Integration tests for HydroLink."""
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from custom_components.hydrolink.const import DOMAIN
from custom_components.hydrolink import async_setup_entry
from homeassistant.config_entries import ConfigEntry

# Test data
MOCK_CONFIG = {
    "domain": DOMAIN,
    "data": {
        "email": "test@example.com",
        "password": "password123"
    }
}

@pytest.mark.asyncio
async def test_setup_and_unload(hass: HomeAssistant):
    """Test setting up and unloading the integration."""
    # Set up the integration
    assert await async_setup_component(hass, DOMAIN, MOCK_CONFIG)
    await hass.async_block_till_done()
    
    # Check if domain is set up
    assert DOMAIN in hass.data
    
    # Create a config entry
    entry = ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="HydroLink Test",
        data=MOCK_CONFIG["data"],
        source="user",
        unique_id="test@example.com"
    )
    
    # Set up entry
    assert await async_setup_entry(hass, entry)
    await hass.async_block_till_done()
    
    # Check if sensors are set up
    sensor_states = hass.states.async_all()
    assert any(state.domain == "sensor" for state in sensor_states)
    
    # Check specific sensors
    water_usage = hass.states.get("sensor.ecowater_softener_water_usage_today")
    assert water_usage is not None
    
    salt_level = hass.states.get("sensor.ecowater_softener_salt_level")
    assert salt_level is not None
    
    # Test sensor attributes
    assert water_usage.attributes["unit_of_measurement"] == "gal"
    assert salt_level.attributes["unit_of_measurement"] == "%"