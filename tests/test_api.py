"""Unit tests for the HydroLink API interface."""
import json
import threading
import time
from unittest.mock import Mock, patch, MagicMock
import pytest
def test_get_data_unauthorized(authenticated_api):
    """Test get_data raises InvalidAuth for 401."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 401
    
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(InvalidAuth):
            authenticated_api.get_data()


def test_get_data_connection_error(authenticated_api):
    """Test get_data raises CannotConnect for connection error."""
    with patch("requests.get", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            authenticated_api.get_data()


import requests
from custom_components.hydrolink.api import (
    HydroLinkApi,
    CannotConnect,
    InvalidAuth,
    Device
)

# Test data
MOCK_EMAIL = "test@example.com"
MOCK_PASSWORD = "password123"
MOCK_AUTH_COOKIE = "test_cookie"
MOCK_DEVICE_ID = "test-device-id"

MOCK_DEVICE_DATA = {
    "deviceId": MOCK_DEVICE_ID,
    "deviceName": "Test Water Softener",
    "model": "Test Model",
    "serialNumber": "123456789",
    "currentWaterFlow": 1.5,
    "waterUsedToday": 45.2,
    "averageDailyUsage": 50.0,
    "saltLevel": 75.5,
    "daysUntilSaltNeeded": 15,
    "onlineStatus": True,
    "wifiSignalStrength": -45,
    "errorCodeAlert": False,
    "hardnessRemoved": 12.5,
    "regenerationStatus": "Ready"
}

@pytest.fixture
def api():
    """Create a HydroLinkApi instance for testing."""
    return HydroLinkApi(MOCK_EMAIL, MOCK_PASSWORD)

@pytest.fixture
def authenticated_api(api, mock_response):
    """Create an authenticated API instance."""
    with patch("requests.post", return_value=mock_response):
        api.login()
    return api

@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.cookies = {"hhfoffoezyzzoeibwv": MOCK_AUTH_COOKIE}
    response.json.return_value = {"data": [MOCK_DEVICE_DATA]}
    response.text = json.dumps({"data": [MOCK_DEVICE_DATA]})
    return response

def test_login_success(api, mock_response):
    """Test successful login."""
    with patch("requests.post", return_value=mock_response):
        assert api.login() is True
        assert api.auth_cookie == MOCK_AUTH_COOKIE

def test_login_invalid_auth(api):
    """Test login with invalid credentials."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 401
    
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(InvalidAuth):
            api.login()

def test_login_connection_error(api):
    """Test login with connection error."""
    with patch("requests.post", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            api.login()

def test_get_data_success(api, mock_response):
    """Test successful data retrieval."""
    # Mock device data
    mock_device_data = {
        "data": [
            {
                "id": MOCK_DEVICE_ID,
                "system_type": "demand_softener",
                "properties": {
                    "water_usage_today": {"value": 100},
                    "salt_level": {"value": 50}
                }
            }
        ]
    }
    mock_response.json = Mock(return_value=mock_device_data)
    
    # Mock WebSocket response
    mock_ws_response = Mock(spec=requests.Response)
    mock_ws_response.status_code = 200
    mock_ws_response.json = Mock(return_value={"websocket_uri": "/ws/test"})
    
    # Mock requests and socket operations
    with patch("requests.get", side_effect=[mock_response, mock_ws_response, mock_response]), \
         patch("requests.post", return_value=mock_response), \
         patch("socket.socket"), \
         patch("websocket.WebSocketApp"):
        # Login first (we know requests.post is mocked)
        api.login()
        # Now get data
        data = api.get_data()
        assert len(data) == 1
        assert data[0]["id"] == MOCK_DEVICE_ID

def test_get_data_no_auth(api):
    """Test data retrieval without authentication."""
    # Create a mock response with 401 status
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 401
    
    with patch("requests.post", return_value=mock_response) as mock_post:
        with pytest.raises(InvalidAuth):
            api.get_data()

def test_get_data_connection_error(api):
    """Test data retrieval with connection error."""
    api.auth_cookie = MOCK_AUTH_COOKIE
    with patch("requests.get", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            api.get_data()

def test_websocket_internal_handling(api):
    """Test that get_data handles websocket internally."""
    api.auth_cookie = MOCK_AUTH_COOKIE
    
    # Test that internal websocket methods exist 
    # but we don't call them directly since they're private
    assert hasattr(api, '_start_ws')
    assert callable(getattr(api, '_start_ws'))


def test_get_data_success(authenticated_api, mock_response):
    """Test get_data method returns device data.""" 
    with patch("requests.get", return_value=mock_response):
        devices = authenticated_api.get_data()
        assert len(devices) == 1
        assert devices[0]["deviceId"] == MOCK_DEVICE_ID


def test_get_data_unauthorized(authenticated_api):
    """Test get_data raises InvalidAuth for 401."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 401
    
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(InvalidAuth):
            authenticated_api.get_data()


def test_get_data_connection_error(authenticated_api):
    """Test get_data raises CannotConnect for connection error."""
    with patch("requests.get", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            authenticated_api.get_data()


def test_get_data_no_auth_cookie(api):
    """Test get_data raises InvalidAuth without auth cookie."""
    # Mock requests.post to avoid socket access during login
    with patch("requests.post") as mock_post:
        # Create a mock response for the login attempt
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        with pytest.raises(InvalidAuth):
            api.get_data()


def test_get_data_unauthorized_v2(authenticated_api):
    """Test device retrieval with unauthorized response."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 401
    
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(InvalidAuth):
            authenticated_api.get_data()


def test_get_data_connection_error_v2(authenticated_api):
    """Test device retrieval with connection error."""
    with patch("requests.get", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            authenticated_api.get_data()


def test_get_data_no_auth_cookie_v2(api):
    """Test device retrieval without authentication."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.ConnectionError
        with pytest.raises(CannotConnect):
            api.get_data()


def test_device_creation_from_data():
    """Test device creation from data dictionary."""
    device = Device(
        id=MOCK_DEVICE_DATA["deviceId"],
        nickname=MOCK_DEVICE_DATA["deviceName"],
        system_type="Advanced",
        properties=MOCK_DEVICE_DATA
    )
    assert device.id == MOCK_DEVICE_ID
    assert device.nickname == "Test Water Softener"


def test_device_creation_missing_fields():
    """Test Device creation with missing fields."""
    minimal_data = {"id": MOCK_DEVICE_ID, "nickname": "Test", "systemType": "Basic"}
    device = Device(
        id=minimal_data["id"],
        nickname=minimal_data["nickname"],
        system_type=minimal_data["systemType"],
        properties=minimal_data
    )
    assert device.id == MOCK_DEVICE_ID
    assert device.nickname == "Test"
    assert device.system_type == "Basic"


def test_trigger_regeneration_success(authenticated_api):
    """Test successful regeneration trigger."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    
    with patch("requests.post", return_value=mock_response):
        result = authenticated_api.trigger_regeneration(MOCK_DEVICE_ID)
        assert result is True


def test_trigger_regeneration_unauthorized(authenticated_api):
    """Test regeneration trigger with unauthorized response."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 401
    
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(InvalidAuth):
            authenticated_api.trigger_regeneration(MOCK_DEVICE_ID)


def test_trigger_regeneration_connection_error(authenticated_api):
    """Test regeneration trigger with connection error."""
    with patch("requests.post", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            authenticated_api.trigger_regeneration(MOCK_DEVICE_ID)


def test_trigger_regeneration_no_auth(api):
    """Test regeneration trigger without authentication."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.ConnectionError
        with pytest.raises(CannotConnect):
            api.trigger_regeneration(MOCK_DEVICE_ID)


def test_api_timeout_error(api):
    """Test API timeout handling."""
    with patch("requests.post", side_effect=requests.Timeout):
        with pytest.raises(CannotConnect):
            api.login()


def test_api_server_error(api):
    """Test API server error handling."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 500
    
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(CannotConnect):
            api.login()


def test_websocket_internal_methods(api):
    """Test WebSocket internal method existence."""
    # Test that internal WebSocket methods exist
    assert hasattr(api, '_start_ws')
    assert callable(getattr(api, '_start_ws'))
    
    # Test that WebSocket URI can be set
    api.ws_uri = "wss://test.example.com/ws"
    assert api.ws_uri == "wss://test.example.com/ws"


def test_device_data_parsing_edge_cases():
    """Test device data parsing with various data types."""
    test_data = {
        "id": MOCK_DEVICE_ID,
        "nickname": "Edge Case Device",
        "systemType": "Advanced",
        "currentWaterFlow": "1.5",  # String instead of float
        "saltLevel": None,  # None value
        "onlineStatus": "true",  # String instead of boolean
        "wifiSignalStrength": "-45",  # String instead of int
    }
    
    device = Device(
        id=test_data["id"],
        nickname=test_data["nickname"],
        system_type=test_data["systemType"],
        properties=test_data
    )
    assert device.id == MOCK_DEVICE_ID
    assert device.properties["currentWaterFlow"] == "1.5"  # Should preserve the string
    assert device.properties["saltLevel"] is None
    assert device.properties["onlineStatus"] == "true"