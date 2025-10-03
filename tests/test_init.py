"""Unit tests for the HydroLink integration."""
from unittest.mock import AsyncMock, Mock, patch
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from custom_components.hydrolink import async_setup_entry, async_unload_entry
from custom_components.hydrolink.const import DOMAIN
from custom_components.hydrolink.const import PLATFORMS

# Test data
MOCK_CONFIG = {
    "email": "test@example.com",
    "password": "password123"
}

@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Create a mock config entry."""
    return ConfigEntry(
        version=1,
        minor_version=1,
        domain=DOMAIN,
        title="HydroLink Test",
        data=MOCK_CONFIG,
        source="user",
        options={},
        unique_id="test@example.com",
        discovery_keys=None
    )

@pytest.fixture
def mock_coordinator(hass: HomeAssistant, mock_config_entry: ConfigEntry) -> Mock:
    """Create a mock data update coordinator."""
    from custom_components.hydrolink.coordinator import HydroLinkDataUpdateCoordinator
    
    coordinator = HydroLinkDataUpdateCoordinator(hass, mock_config_entry)
    coordinator.async_setup = Mock(return_value=True)
    coordinator.async_config_entry_first_refresh = AsyncMock()
    return coordinator

@pytest.mark.asyncio
async def test_setup_entry(hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock):
    """Test setting up the integration."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {}
    
    with patch("custom_components.hydrolink.coordinator.HydroLinkDataUpdateCoordinator", return_value=mock_coordinator):
        result = await async_setup_entry(hass, mock_config_entry)
        
    assert result is True
    assert DOMAIN in hass.data
    assert mock_config_entry.entry_id in hass.data[DOMAIN]
    assert hass.data[DOMAIN][mock_config_entry.entry_id] == mock_coordinator
    hass.config_entries.async_forward_entry_setups.assert_called_once_with(mock_config_entry, PLATFORMS)

@pytest.mark.asyncio
async def test_unload_entry(hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock):
    """Test unloading the integration."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {DOMAIN: {mock_config_entry.entry_id: mock_coordinator}}
    
    result = await async_unload_entry(hass, mock_config_entry)
    assert result is True
    assert mock_config_entry.entry_id not in hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_setup_entry_coordinator_failure(hass: HomeAssistant, mock_config_entry: ConfigEntry):
    """Test setup with coordinator initialization failure."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {}
    
    # Mock coordinator that fails setup
    mock_coordinator = Mock()
    mock_coordinator.async_config_entry_first_refresh = AsyncMock(side_effect=Exception("Setup failed"))
    
    with patch("custom_components.hydrolink.coordinator.HydroLinkDataUpdateCoordinator", return_value=mock_coordinator):
        result = await async_setup_entry(hass, mock_config_entry)
        
    assert result is False


@pytest.mark.asyncio
async def test_setup_entry_forward_setup_failure(hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock):
    """Test setup with platform forward setup failure."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {}
    
    # Mock forward_entry_setups to fail
    hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=False)
    
    with patch("custom_components.hydrolink.coordinator.HydroLinkDataUpdateCoordinator", return_value=mock_coordinator):
        result = await async_setup_entry(hass, mock_config_entry)
        
    assert result is False


@pytest.mark.asyncio
async def test_unload_entry_forward_unload_failure(hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock):
    """Test unload with platform forward unload failure."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {DOMAIN: {mock_config_entry.entry_id: mock_coordinator}}
    
    # Mock forward_entry_unload to fail
    hass.config_entries.async_forward_entry_unload = AsyncMock(return_value=False)
    
    result = await async_unload_entry(hass, mock_config_entry)
    assert result is False


@pytest.mark.asyncio
async def test_unload_entry_not_loaded(hass: HomeAssistant, mock_config_entry: ConfigEntry):
    """Test unloading an entry that wasn't properly loaded."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {DOMAIN: {}}  # Entry not in data
    
    result = await async_unload_entry(hass, mock_config_entry)
    # Should still return True even if entry wasn't in data
    assert result is True


@pytest.mark.asyncio
async def test_setup_entry_no_domain_data(hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock):
    """Test setup when domain data doesn't exist yet."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {}  # No domain data yet
    
    with patch("custom_components.hydrolink.coordinator.HydroLinkDataUpdateCoordinator", return_value=mock_coordinator):
        result = await async_setup_entry(hass, mock_config_entry)
        
    assert result is True
    assert DOMAIN in hass.data
    assert mock_config_entry.entry_id in hass.data[DOMAIN]