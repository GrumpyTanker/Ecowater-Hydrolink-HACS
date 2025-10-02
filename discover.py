# -*- coding: utf-8 -*-
"""
A script to discover all available data points from the HydroLink API.

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
import argparse
import json
import logging
import sys
import os

# This is a workaround to allow the script to import the api module directly
# without triggering the homeassistant-specific parts of the integration.
sys.path.append(os.path.join(os.path.dirname(__file__), 'custom_components/hydrolink'))

from api import HydroLinkApi, CannotConnect, InvalidAuth

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
_LOGGER = logging.getLogger(__name__)

def discover_data(email, password):
    """Connect to the HydroLink API and save all available data to a file.

    Args:
        email: The user's HydroLink email address.
        password: The user's HydroLink password.
    """
    _LOGGER.info("Attempting to connect to HydroLink API...")
    
    try:
        # Initialize the API
        api = HydroLinkApi(email, password)
        
        # Log in
        api.login()
        
        # Fetch the data
        _LOGGER.info("Login successful. Fetching device data...")
        data = api.get_data()
        
        # Save the data to a file
        script_dir = os.path.dirname(__file__)
        output_filename = os.path.join(script_dir, "discovery_output.json")
        _LOGGER.info(f"Successfully fetched data. Writing to {output_filename}...")
        with open(output_filename, "w") as f:
            json.dump(data, f, indent=2)
        _LOGGER.info(f"Data successfully written to {output_filename}")
        
    except InvalidAuth:
        _LOGGER.error("Authentication failed. Please check your email and password.")
        sys.exit(1)
    except CannotConnect as e:
        _LOGGER.error(f"Could not connect to the API: {e}")
        sys.exit(1)
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover HydroLink API data points.")
    parser.add_argument("--email", required=True, help="Your HydroLink email address.")
    parser.add_argument("--password", required=True, help="Your HydroLink password.")
    
    args = parser.parse_args()
    
    discover_data(args.email, args.password)
