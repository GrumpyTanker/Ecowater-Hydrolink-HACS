"""Test the config flow."""
from unittest.mock import AsyncMock, Mock, patch
import pytest
from homeassistant import config_entries, data_entry_flow
from custom_components.hydrolink.const import DOMAIN
from custom_components.hydrolink.config_flow import ConfigFlow
from custom_components.hydrolink.api import CannotConnect, InvalidAuth
from .helpers import create_mock_hass

# Test data
MOCK_EMAIL = "test@example.com"
MOCK_PASSWORD = "password123"

def setup_mock_flow():
    """Set up a config flow with mocked hass instance."""
    # Create and initialize the flow with a mocked hass instance
    flow = ConfigFlow()
    flow.hass = create_mock_hass()
    return flow

@pytest.mark.asyncio
async def test_form():
    """Test showing the form."""
    flow = setup_mock_flow()
    
    result = await flow.async_step_user()
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"

@pytest.mark.asyncio
async def test_user_input_validation():
    """Test input validation."""
    flow = setup_mock_flow()
    
    # Test with empty email
    result = await flow.async_step_user({"email": "", "password": MOCK_PASSWORD})
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}
    
    # Test with empty password
    result = await flow.async_step_user({"email": MOCK_EMAIL, "password": ""})
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}

@pytest.mark.asyncio
async def test_successful_config_flow():
    """Test a successful config flow."""
    flow = setup_mock_flow()
    
    # Mock async_set_unique_id to do nothing
    mock_set_unique_id = Mock()
    mock_set_unique_id.return_value = None
    flow.async_set_unique_id = mock_set_unique_id
    
    # Mock _abort_if_unique_id_configured to do nothing
    flow._abort_if_unique_id_configured = Mock()
    
    with patch(
        "custom_components.hydrolink.api.HydroLinkApi.login",
        return_value=True,
    ):
        result = await flow.async_step_user({
            "email": MOCK_EMAIL,
            "password": MOCK_PASSWORD,
        })
        
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == MOCK_EMAIL
    assert result["data"] == {
        "email": MOCK_EMAIL,
        "password": MOCK_PASSWORD,
    }

@pytest.mark.asyncio
async def test_failed_config_flow_invalid_auth():
    """Test a failed config flow due to invalid auth."""
    flow = setup_mock_flow()
    
    with patch(
        "custom_components.hydrolink.api.HydroLinkApi.login",
        side_effect=InvalidAuth,
    ):
        result = await flow.async_step_user({
            "email": MOCK_EMAIL,
            "password": MOCK_PASSWORD,
        })
        
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}

@pytest.mark.asyncio
async def test_failed_config_flow_cannot_connect():
    """Test a failed config flow due to connection error."""
    flow = setup_mock_flow()
    
    with patch(
        "custom_components.hydrolink.api.HydroLinkApi.login",
        side_effect=CannotConnect,
    ):
        result = await flow.async_step_user({
            "email": MOCK_EMAIL,
            "password": MOCK_PASSWORD,
        })
        
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}