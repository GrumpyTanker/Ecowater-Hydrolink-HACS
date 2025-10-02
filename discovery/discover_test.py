# -*- coding: utf-8 -*-
"""EcoWater HydroLink API Discovery Tool"""
import argparse
import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add custom_components to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_components/hydrolink"))
from api import HydroLinkApi

# Setup
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

def clean_data(device: Dict) -> Dict:
    """Clean and organize device data."""
    result = {
        "device": {
            "id": device.get("id"),
            "type": device.get("system_type"),
            "model": device.get("model_description", device.get("system_type_display")),
            "serial": device.get("product_serial_number"),
            "nickname": device.get("nickname"),
            "location": device.get("location"),
            "image_url": device.get("image_url")
        },
        "status": {
            "is_online": False,
            "state": None,
            "last_updated": None,
            "signal_strength": None,
            "signal_bars": None
        },
        "metrics": {
            "daily": {
                "usage": None,
                "average_usage": None,
                "rock_removed": None
            },
            "current": {
                "flow_rate": None,
                "total_usage": None,
                "treated_water_remaining": None,
                "capacity_remaining": None
            },
            "lifetime": {
                "total_usage": None,
                "total_regens": None,
                "rock_removed": None,
                "days_in_operation": None,
                "days_since_regen": None,
                "time_lost_events": None
            }
        },
        "maintenance": {
            "salt": {
                "level": None,
                "days_remaining": None,
                "low_alert": None,
                "efficiency": None,
                "total_usage": None,
                "avg_per_regen": None,
                "type": None
            },
            "service": {
                "active": None,
                "reminder_months": None,
                "reminder_alert": None
            },
            "errors": {
                "code": None,
                "alert": None,
                "leak_alert": None,
                "flow_alert": None
            }
        },
        "settings": {}
    }
    
    # Process properties
    props = device.get("properties", {})
    for key, data in props.items():
        value = data.get("value")
        updated = data.get("updated_at")
        
        # Online status
        if key == "_internal_is_online":
            result["status"]["is_online"] = value
            result["status"]["last_updated"] = updated
        elif key == "rf_signal_strength_dbm":
            result["status"]["signal_strength"] = value
        elif key == "rf_signal_bars":
            result["status"]["signal_bars"] = value
            
        # Daily metrics
        elif key == "gallons_used_today":
            result["metrics"]["daily"]["usage"] = {"value": value, "updated": updated}
        elif key == "avg_daily_use_gals":
            result["metrics"]["daily"]["average_usage"] = {"value": value, "updated": updated}
        elif key == "daily_avg_rock_removed_lbs":
            result["metrics"]["daily"]["rock_removed"] = {"value": value, "updated": updated}
            
        # Current metrics
        elif key == "current_water_flow_gpm":
            result["metrics"]["current"]["flow_rate"] = {"value": value, "updated": updated}
        elif key == "water_counter_gals":
            result["metrics"]["current"]["total_usage"] = {"value": value, "updated": updated}
        elif key == "treated_water_avail_gals":
            result["metrics"]["current"]["treated_water_remaining"] = {"value": value, "updated": updated}
        elif key == "capacity_remaining_percent":
            result["metrics"]["current"]["capacity_remaining"] = {"value": value, "updated": updated}
            
        # Lifetime metrics
        elif key == "total_outlet_water_gals":
            result["metrics"]["lifetime"]["total_usage"] = {"value": value, "updated": updated}
        elif key == "total_regens":
            result["metrics"]["lifetime"]["total_regens"] = {"value": value, "updated": updated}
        elif key == "total_rock_removed_lbs":
            result["metrics"]["lifetime"]["rock_removed"] = {"value": value, "updated": updated}
        elif key == "days_in_operation":
            result["metrics"]["lifetime"]["days_in_operation"] = {"value": value, "updated": updated}
        elif key == "days_since_last_regen":
            result["metrics"]["lifetime"]["days_since_regen"] = {"value": value, "updated": updated}
        elif key == "time_lost_events":
            result["metrics"]["lifetime"]["time_lost_events"] = {"value": value, "updated": updated}
            
        # Salt management
        elif key == "salt_level_tenths":
            result["maintenance"]["salt"]["level"] = {"value": value / 10, "updated": updated}
        elif key == "out_of_salt_estimate_days":
            result["maintenance"]["salt"]["days_remaining"] = {"value": value, "updated": updated}
        elif key == "low_salt_alert":
            result["maintenance"]["salt"]["low_alert"] = {"value": value, "updated": updated}
        elif key == "salt_effic_grains_per_lb":
            result["maintenance"]["salt"]["efficiency"] = {"value": value, "updated": updated}
        elif key == "total_salt_use_lbs":
            result["maintenance"]["salt"]["total_usage"] = {"value": value, "updated": updated}
        elif key == "avg_salt_per_regen_lbs":
            result["maintenance"]["salt"]["avg_per_regen"] = {"value": value / 1000, "updated": updated}
        elif key == "salt_type_enum":
            result["maintenance"]["salt"]["type"] = {"value": value, "updated": updated}
            
        # Service info
        elif key == "service_active":
            result["maintenance"]["service"]["active"] = {"value": value, "updated": updated}
        elif key == "service_reminder_months":
            result["maintenance"]["service"]["reminder_months"] = {"value": value, "updated": updated}
        elif key == "service_reminder_alert":
            result["maintenance"]["service"]["reminder_alert"] = {"value": value, "updated": updated}
            
        # Error info
        elif key == "error_code":
            result["maintenance"]["errors"]["code"] = {"value": value, "updated": updated}
        elif key == "error_code_alert":
            result["maintenance"]["errors"]["alert"] = {"value": value, "updated": updated}
        elif key == "floor_leak_detector_alert":
            result["maintenance"]["errors"]["leak_alert"] = {"value": value, "updated": updated}
        elif key == "flow_monitor_alert":
            result["maintenance"]["errors"]["flow_alert"] = {"value": value, "updated": updated}
            
        # Keep important settings
        elif key in [
            "hardness_grains", 
            "iron_level_tenths_ppm",
            "operating_capacity_grains",
            "regen_time_secs",
            "model_display_code",
            "base_software_version",
            "esp_software_part_number"
        ]:
            result["settings"][key] = {"value": value, "updated": updated}
    
    return result

def main(args):
    """Run the discovery tool."""
    api = HydroLinkApi(args.email, args.password)

    # Get device data
    devices = api.get_data()
    cleaned_devices = [clean_data(device) for device in devices]

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save raw data for comparison
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_filename = f"discovery_raw_{timestamp}.json"
    raw_filepath = os.path.join(OUTPUT_DIR, raw_filename)
    with open(raw_filepath, "w") as f:
        json.dump(devices, f, indent=4)
    _LOGGER.info(f"Raw data saved to {raw_filepath}")

    # Save cleaned data
    clean_filename = f"discovery_cleaned_{timestamp}.json"
    clean_filepath = os.path.join(OUTPUT_DIR, clean_filename)
    with open(clean_filepath, "w") as f:
        json.dump(cleaned_devices, f, indent=4)
    _LOGGER.info(f"Cleaned data saved to {clean_filepath}")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="HydroLink Discovery Tool")
    parser.add_argument("--email", required=True, help="HydroLink account email")
    parser.add_argument("--password", required=True, help="HydroLink account password")
    args = parser.parse_args()
    
    main(args)