# -*- coding: utf-8 -*-
"""
EcoWater HydroLink API Discovery Tool

Utility script for discovering and analyzing data from the API.
"""
import argparse
import json
import logging
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_components/hydrolink"))
from api import HydroLinkApi

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

def discover():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    api = HydroLinkApi(args.email, args.password)
    data = api.get_data()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"discovery_{timestamp}.json")
    
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    _LOGGER.info(f"Data written to {output_file}")

if __name__ == "__main__":
    discover()
