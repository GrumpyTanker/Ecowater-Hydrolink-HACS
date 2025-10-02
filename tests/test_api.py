"""Unit tests for the HydroLink API interface."""
import json
import threading
import time
from unittest.mock import Mock, patch
import pytest
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

@pytest.fixture
def api():
    """Create a HydroLinkApi instance for testing."""
    return HydroLinkApi(MOCK_EMAIL, MOCK_PASSWORD)

@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.cookies = {"hhfoffoezyzzoeibwv": MOCK_AUTH_COOKIE}
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
    
    with patch("requests.get", side_effect=[mock_response, mock_ws_response, mock_response]):
        with patch("websocket.WebSocketApp"):
            data = api.get_data()
            assert len(data) == 1
            assert data[0]["id"] == MOCK_DEVICE_ID

def test_get_data_no_auth(api):
    """Test data retrieval without authentication."""
    with pytest.raises(InvalidAuth):
        api.get_data()

def test_get_data_connection_error(api):
    """Test data retrieval with connection error."""
    api.auth_cookie = MOCK_AUTH_COOKIE
    with patch("requests.get", side_effect=requests.ConnectionError):
        with pytest.raises(CannotConnect):
            api.get_data()

def test_websocket_message_handling(api):
    """Test WebSocket message handling."""
    api.ws_uri = "wss://test.com/ws"
    api.auth_cookie = "test_cookie"  # Need to be authenticated
    
    # Mock WebSocket
    mock_ws = Mock()
    mock_ws.run_forever = Mock()  # Prevent actual WebSocket connection
    
    with patch("websocket.WebSocketApp", return_value=mock_ws):
        # Start WebSocket in separate thread
        ws_thread = threading.Thread(target=api._start_ws)
        ws_thread.start()
        
        # Give thread time to start
        time.sleep(0.1)
        
        # Simulate message reception
        on_message = mock_ws.on_message
        message_data = {"test": "data"}
        on_message(mock_ws, json.dumps(message_data))
        
        # Give time for message processing
        time.sleep(0.1)
        
        # Verify message tracking
        assert api.ws_message_count == 1
        
        # Test automatic close after 17 messages
        for _ in range(16):
            on_message(mock_ws, json.dumps(message_data))
            
        assert mock_ws.close.called
        
        # Wait for thread to finish
        ws_thread.join(timeout=1)