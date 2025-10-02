# -*- coding: utf-8 -*-
"""
API for HydroLink.

Copyright 2025 GrumpyTanker

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import requests
import websocket
import threading
import time

_LOGGER = logging.getLogger(__name__)


class HydroLinkApi:
    """The API for HydroLink devices."""

    def __init__(self, email, password):
        """Initialize the API.

        Args:
            email: The user's HydroLink email.
            password: The user's HydroLink password.
        """
        self.email = email
        self.password = password
        self.auth_cookie = None
        self.ws_message_count = 0
        self.waiting_for_ws_thread_to_end = 1
        self.ws_uri = ""

    def login(self):
        """Login to the HydroLink API.

        Raises:
            InvalidAuth: If the credentials are invalid.
            CannotConnect: If there is a connection error.

        Returns:
            True if login is successful.
        """
        try:
            r = requests.post(
                "https://api.hydrolinkhome.com/v1/auth/login",
                json={"email": self.email, "password": self.password},
                timeout=10,
            )
            r.raise_for_status()
            self.auth_cookie = r.cookies.get("hhfoffoezyzzoeibwv")
            _LOGGER.info("HydroLink login successful")
            return True
        except requests.HTTPError as err:
            if err.response.status_code == 401:
                raise InvalidAuth from err
            raise CannotConnect from err
        except requests.RequestException as err:
            raise CannotConnect from err

    def _start_ws(self):
        """Start the WebSocket client.

        This function runs in a separate thread and closes the connection
        after receiving a certain number of messages. This is intended to
        trigger a data refresh on the server.
        """
        def on_message(ws, message):
            """Handle incoming WebSocket messages."""
            self.ws_message_count += 1
            # The web app seems to close after 17 messages.
            if self.ws_message_count >= 17:
                ws.close()

        def on_open(ws):
            """Handle WebSocket connection open."""
            _LOGGER.debug("HydroLink WebSocket opened")

        def on_close(ws, close_status_code, close_msg):
            """Handle WebSocket connection close."""
            _LOGGER.debug(f"HydroLink WebSocket closed: {close_status_code} {close_msg}")

        def on_error(ws, error):
            """Handle WebSocket errors."""
            _LOGGER.error(f"HydroLink WebSocket error: {error}")

        self.ws_message_count = 0
        ws = websocket.WebSocketApp(
            self.ws_uri,
            on_message=on_message,
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
        )
        ws.run_forever()
        self.waiting_for_ws_thread_to_end = 0

    def get_data(self):
        """Get the latest data from the HydroLink API.

        This function logs in if necessary, then fetches the list of devices.
        For each device, it triggers a data refresh by opening a WebSocket
        connection, and then fetches the updated device data.

        Raises:
            CannotConnect: If there is a connection error.

        Returns:
            A list of devices with their properties.
        """
        if not self.auth_cookie:
            self.login()

        try:
            # Get the list of devices
            r = requests.get(
                "https://api.hydrolinkhome.com/v1/devices?all=false&per_page=200",
                cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                timeout=10,
            )
            r.raise_for_status()
            devices = r.json().get("data", [])

            # For each device, trigger a data refresh via WebSocket
            for dev in devices:
                dev_id = dev.get("id")
                # Get the WebSocket URI for the device
                r = requests.get(
                    f"https://api.hydrolinkhome.com/v1/devices/{dev_id}/live",
                    cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                    timeout=10,
                )
                r.raise_for_status()

                # Start the WebSocket client in a new thread
                self.ws_uri = r.json().get("websocket_uri") or {}
                self.ws_uri = f"wss://api.hydrolinkhome.com{self.ws_uri}"
                self.waiting_for_ws_thread_to_end = 1
                
                ws_thread = threading.Thread(target=self._start_ws, daemon=True)
                ws_thread.start()
                
                # Wait for the WebSocket thread to complete
                num_of_waits = 0
                while self.waiting_for_ws_thread_to_end:
                    time.sleep(1)
                    num_of_waits += 1
                    if num_of_waits > 15:
                        _LOGGER.warning("HydroLink WebSocket thread took too long to complete.")
                        break
                
                ws_thread.join(timeout=5)

            # Fetch the fresh data
            r = requests.get(
                "https://api.hydrolinkhome.com/v1/devices?all=false&per_page=200",
                cookies={"hhfoffoezyzzoeibwv": self.auth_cookie},
                timeout=10,
            )
            r.raise_for_status()
            return r.json().get("data", [])

        except requests.RequestException as err:
            raise CannotConnect from err


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
