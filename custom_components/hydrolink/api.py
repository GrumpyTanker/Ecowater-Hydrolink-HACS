# -*- coding: utf-8 -*-
"""
EcoWater HydroLink API Interface for Home Assistant

A Python interface for interacting with EcoWater's HydroLink cloud service.
This module handles authentication, data retrieval, and real-time updates
through WebSocket connections.

Based on the original Hydrolink-Home-Status project:
https://github.com/GrumpyTanker/Hydrolink-Home-Status

This version adds HACS compatibility, real-time WebSocket updates,
improved error handling, and comprehensive data organization.

Author: GrumpyTanker
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release based on Hydrolink-Home-Status
  * Basic API implementation
  * Device data retrieval
  
- 0.2.0 (2025-10-02)
  * Added WebSocket support for real-time updates
  * Added HACS compatibility
  * Improved error handling and logging
  * Added type hints and dataclass models
  * Enhanced data organization and cleaning
  * Added example data for development
  
- 0.3.0 (2025-10-02)
  * Added comprehensive documentation of all sensors
  * Added diagnostic sensors section
  * Improved data cleaning and organization
  * Enhanced example data with complete attribute descriptions
  * Added discovery tools for development

License: MIT
See LICENSE file in the project root for full license information.
"""

Typical usage example:

    api = HydroLinkApi("user@example.com", "password")
    api.login()
    data = api.get_data()
"""

import logging
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json
import logging
import requests
import websocket
import threading
import time

_LOGGER = logging.getLogger(__name__)


@dataclass
class Device:
    """Represents a HydroLink device."""

    id: str
    nickname: str
    system_type: str
    properties: Dict[str, Any]

class HydroLinkApi:
    """Interface to the HydroLink API.
    
    This class provides methods to authenticate with the HydroLink service
    and retrieve data from connected water softener devices.
    
    Attributes:
        email: The user's HydroLink account email.
        password: The user's HydroLink account password.
        auth_cookie: Authentication cookie from successful login.
        ws_message_count: Counter for WebSocket messages received.
        waiting_for_ws_thread_to_end: Flag for WebSocket thread status.
        ws_uri: WebSocket connection URI.
        BASE_URL: Base URL for the HydroLink API.
        WS_BASE_URL: Base URL for WebSocket connections.
    """

    BASE_URL = "https://api.hydrolinkhome.com/v1"
    WS_BASE_URL = "wss://api.hydrolinkhome.com"

    def __init__(self, email: str, password: str) -> None:
        """Initialize the API.

        Args:
            email: The user's HydroLink email.
            password: The user's HydroLink password.
        """
        self.email: str = email
        self.password: str = password
        self.auth_cookie: Optional[str] = None
        self.ws_message_count: int = 0
        self.waiting_for_ws_thread_to_end: int = 1
        self.ws_uri: str = ""

    def login(self) -> bool:
        """Authenticate with the HydroLink API.

        Performs authentication using the provided email and password.
        Stores the authentication cookie for subsequent requests.

        Raises:
            InvalidAuth: If the credentials are invalid.
            CannotConnect: If there is a connection or timeout error.

        Returns:
            bool: True if login is successful.

        Example:
            >>> api = HydroLinkApi("user@example.com", "password")
            >>> api.login()
            True
        """
        try:
            response = requests.post(
                f"{self.BASE_URL}/auth/login",
                json={
                    "email": self.email,
                    "password": self.password
                },
                timeout=10,
            )
            
            # Check for specific error responses
            if response.status_code == 401:
                raise InvalidAuth("Invalid email or password")
            elif response.status_code == 429:
                raise CannotConnect("Rate limit exceeded")
            elif response.status_code >= 500:
                raise CannotConnect(f"Server error: {response.status_code}")
            
            response.raise_for_status()
            
            # Get authentication cookie
            self.auth_cookie = response.cookies.get("hhfoffoezyzzoeibwv")
            if not self.auth_cookie:
                raise CannotConnect("No authentication cookie received")
            
            _LOGGER.info("HydroLink login successful")
            return True
            
        except requests.Timeout:
            raise CannotConnect("Connection timed out") from None
        except requests.ConnectionError:
            raise CannotConnect("Failed to connect to HydroLink") from None
        except requests.RequestException as err:
            raise CannotConnect(f"Unknown error: {err}") from err

    def _start_ws(self) -> None:
        """Start the WebSocket client for real-time updates.

        This function runs in a separate thread and establishes a WebSocket
        connection to receive real-time updates from the device. It automatically
        closes the connection after receiving a predetermined number of messages
        to trigger a data refresh on the server.

        The WebSocket connection is used to ensure the device sends fresh data
        when we make subsequent REST API calls.

        Note:
            The web app closes the connection after 17 messages, so we follow
            the same pattern to maintain compatibility.
        """
        def on_message(ws: websocket.WebSocketApp, message: str) -> None:
            """Handle incoming WebSocket messages.
            
            Args:
                ws: The WebSocket connection instance.
                message: The received message string.
            """
            try:
                # Increment message counter
                self.ws_message_count += 1
                
                # Parse and log message if in debug mode
                if _LOGGER.isEnabledFor(logging.DEBUG):
                    data = json.loads(message)
                    _LOGGER.debug("Received WebSocket message: %s", data)
                
                # Close after receiving expected number of messages
                if self.ws_message_count >= 17:
                    ws.close()
                    
            except json.JSONDecodeError as err:
                _LOGGER.warning("Failed to parse WebSocket message: %s", err)

        def on_open(ws: websocket.WebSocketApp) -> None:
            """Handle WebSocket connection open event.
            
            Args:
                ws: The WebSocket connection instance.
            """
            _LOGGER.debug("HydroLink WebSocket connection established")

        def on_close(ws: websocket.WebSocketApp, close_status_code: int, 
                    close_msg: str) -> None:
            """Handle WebSocket connection close event.
            
            Args:
                ws: The WebSocket connection instance.
                close_status_code: The WebSocket close status code.
                close_msg: The close message if any.
            """
            _LOGGER.debug("HydroLink WebSocket closed: %s %s", 
                         close_status_code, close_msg)

        def on_error(ws: websocket.WebSocketApp, error: Exception) -> None:
            """Handle WebSocket errors.
            
            Args:
                ws: The WebSocket connection instance.
                error: The error that occurred.
            """
            _LOGGER.error("HydroLink WebSocket error: %s", error)

        try:
            # Reset message counter
            self.ws_message_count = 0
            
            # Create and run WebSocket connection
            ws = websocket.WebSocketApp(
                self.ws_uri,
                on_message=on_message,
                on_open=on_open,
                on_close=on_close,
                on_error=on_error,
            )
            ws.run_forever()
            
        except Exception as err:
            _LOGGER.error("WebSocket connection failed: %s", err)
            raise CannotConnect("WebSocket connection failed") from err
            
        finally:
            # Signal thread completion
            self.waiting_for_ws_thread_to_end = 0

    def get_data(self) -> List[Dict[str, Any]]:
        """Get the latest data from the HydroLink API.

        This method performs the following steps:
        1. Ensures authentication is current
        2. Fetches the list of devices
        3. For each device:
           - Gets the WebSocket URI
           - Opens a WebSocket connection to trigger data refresh
           - Waits for the refresh to complete
        4. Fetches and returns the updated device data

        The WebSocket connection is used to ensure we get fresh data rather
        than cached values from the API.

        Raises:
            InvalidAuth: If authentication has expired or is invalid.
            CannotConnect: If there are connection issues.
            TimeoutError: If operations take too long to complete.

        Returns:
            List[Dict[str, Any]]: A list of devices with their properties.

        Example:
            >>> api = HydroLinkApi("user@example.com", "password")
            >>> api.login()
            >>> data = api.get_data()
            >>> print(data[0]["properties"]["water_usage_today"])
        """
        # Ensure we're authenticated
        if not self.auth_cookie:
            self.login()

        try:
            # Get the list of devices
            response = requests.get(
                f"{self.BASE_URL}/devices",
                params={"all": "false", "per_page": "200"},
                cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                timeout=10,
            )
            
            # Handle authentication errors
            if response.status_code == 401:
                self.auth_cookie = None
                raise InvalidAuth("Authentication expired")
                
            response.raise_for_status()
            devices = response.json().get("data", [])

            # Process each device
            for device in devices:
                try:
                    device_id = device.get("id")
                    if not device_id:
                        _LOGGER.warning("Device without ID found, skipping")
                        continue

                    # Get the WebSocket URI for the device
                    response = requests.get(
                        f"{self.BASE_URL}/devices/{device_id}/live",
                        cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                        timeout=10,
                    )
                    response.raise_for_status()

                    # Extract and format WebSocket URI
                    ws_path = response.json().get("websocket_uri")
                    if not ws_path:
                        _LOGGER.warning("No WebSocket URI for device %s", device_id)
                        continue
                        
                    self.ws_uri = f"{self.WS_BASE_URL}{ws_path}"
                    self.waiting_for_ws_thread_to_end = 1
                    
                    # Start WebSocket connection in separate thread
                    ws_thread = threading.Thread(
                        target=self._start_ws,
                        name=f"HydroLink-WS-{device_id}",
                        daemon=True
                    )
                    ws_thread.start()
                    
                    # Wait for WebSocket thread to complete
                    start_time = time.time()
                    while self.waiting_for_ws_thread_to_end:
                        time.sleep(0.5)
                        if time.time() - start_time > 15:
                            _LOGGER.warning(
                                "WebSocket thread timeout for device %s",
                                device_id
                            )
                            break
                    
                    # Ensure thread terminates
                    ws_thread.join(timeout=5)
                    if ws_thread.is_alive():
                        _LOGGER.warning(
                            "WebSocket thread did not terminate for device %s",
                            device_id
                        )

                except requests.RequestException as err:
                    _LOGGER.error(
                        "Error refreshing device %s: %s",
                        device.get("id", "unknown"),
                        err
                    )

            # Fetch fresh data for all devices
            response = requests.get(
                f"{self.BASE_URL}/devices",
                params={"all": "false", "per_page": "200"},
                cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                timeout=10,
            )
            response.raise_for_status()
            
            return response.json().get("data", [])

        except requests.Timeout:
            raise CannotConnect("Connection timed out") from None
        except requests.ConnectionError:
            raise CannotConnect("Failed to connect to HydroLink") from None
        except requests.RequestException as err:
            raise CannotConnect(f"Error fetching device data: {err}") from err


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


    def trigger_regeneration(self, device_id: str) -> bool:
        """Trigger a manual regeneration for a specific device.
        
        Args:
            device_id: The ID of the device to regenerate.
            
        Returns:
            bool: True if regeneration was successfully triggered.
            
        Raises:
            CannotConnect: If there is a connection error.
            InvalidAuth: If authentication has expired.
        """
        if not self.auth_cookie:
            self.login()
            
        try:
            response = requests.post(
                f"{self.BASE_URL}/devices/{device_id}/regenerate",
                cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                timeout=10
            )
            
            if response.status_code == 401:
                self.auth_cookie = None
                raise InvalidAuth("Authentication expired")
                
            response.raise_for_status()
            return True
            
        except requests.Timeout:
            raise CannotConnect("Connection timed out") from None
        except requests.ConnectionError:
            raise CannotConnect("Failed to connect to HydroLink") from None
        except requests.RequestException as err:
            raise CannotConnect(f"Error triggering regeneration: {err}") from err


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
