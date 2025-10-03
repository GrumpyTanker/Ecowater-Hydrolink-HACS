# EcoWater HydroLink Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/workflows/Validate/badge.svg)](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/actions)
[![Run Tests](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/workflows/Run%20Tests/badge.svg)](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/actions)
[![HA Core Version](https://img.shields.io/badge/Home%20Assistant-2024.10.0+-blue.svg)](https://www.home-assistant.io)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)

A Home Assistant integration for EcoWater's HydroLink connected water softeners. Monitor your water softener's performance, water usage, salt levels, and more directly in Home Assistant with real-time updates.

This integration is a HACS-compatible adaptation of the original [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status) project, enhanced with improved data organization, real-time WebSocket updates, comprehensive error handling, and full Home Assistant integration.

## Key Features

- 🔄 Real-time monitoring via WebSocket connections
- 📊 30+ sensors across 8 comprehensive categories
- 🔧 Service calls for manual regeneration control
- 🏠 Full Home Assistant integration with proper device modeling
- 📈 Historical data tracking and analytics
- 🚨 Alert notifications for system issues
- 🔒 Secure authentication with EcoWater cloud services
- 📱 Mobile-friendly interface

## Sensor Categories

### Basic System Information
- Online Status, Model, Device Name, Serial Number

### Water Usage Monitoring  
- Current Flow, Daily/Weekly/Monthly Usage, Peak Flow Statistics

### Salt Management
- Salt Level, Days Remaining, Usage Statistics, Efficiency Tracking

### System Performance
- Capacity Remaining, Water Hardness, Treatment Statistics

### Regeneration Management
- Current Status, History, Scheduling, Manual Control

### Critical Alerts
- Low Salt Warnings, System Errors, Flow Anomalies, Leak Detection

### Signal and Connection
- WiFi Strength, Connection Quality, Network Status

### Maintenance Information
- Service Reminders, Operation Statistics, System Health

## Installation

### HACS Installation (Preferred)
1. Ensure you have [HACS](https://hacs.xyz) installed in your Home Assistant instance
2. Search for "EcoWater HydroLink" in HACS
3. Click Install
4. Restart Home Assistant
5. Add the integration via the Home Assistant UI:
   - Go to Settings → Devices & Services
   - Click the "+ ADD INTEGRATION" button
   - Search for "EcoWater HydroLink"
6. Enter your HydroLink credentials when prompted

### Manual Installation
1. Download the latest release from the GitHub repository
2. Copy the `custom_components/hydrolink` directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services in Home Assistant
2. Click "Add Integration"
3. Search for "HydroLink"
4. Enter your HydroLink email and password
5. Click "Submit"

## Available Sensors

### Water Usage and Flow
| Sensor | Description | Unit |
|--------|-------------|------|
| Current Water Flow | Current water flow rate | GPM |
| Water Used Today | Today's water consumption | Gallons |
| Average Daily Usage | Average daily water usage | Gallons |
| Total Treated Water | Total treated water volume | Gallons |
| Peak Water Flow | Peak water flow rate | GPM |
| Available Treated Water | Available treated water | Gallons |

### Salt Management
| Sensor | Description | Unit |
|--------|-------------|------|
| Salt Level | Current salt level | % |
| Days Until Salt Needed | Estimated days until salt refill | Days |
| Average Salt Per Regeneration | Salt used per regeneration cycle | lbs |
| Total Salt Used | Total salt consumption | lbs |

### System Performance
| Sensor | Description | Unit |
|--------|-------------|------|
| Remaining Capacity | Remaining treatment capacity | % |
| Operating Capacity | System operating capacity | Grains |
| Water Hardness | Current water hardness level | Grains |
| Hardness Removed (Recent) | Hardness removed since last recharge | lbs |
| Daily Average Hardness Removed | Average daily hardness removal | lbs |
| Total Hardness Removed | Total lifetime hardness removal | lbs |

### Regeneration Status
| Sensor | Description | Unit |
|--------|-------------|------|
| Regeneration Status | Current regeneration state | - |
| Days Since Last Regeneration | Time since last regeneration | Days |
| Total Regenerations | Total regeneration cycles | Count |
| Manual Regenerations | Manual regeneration count | Count |
| Remaining Regeneration Time | Time left in current cycle | Minutes |

### System Health and Alerts
| Sensor | Description | Unit |
|--------|-------------|------|
| Low Salt Alert | Salt level warning status | - |
| Error Code Alert | System error indicator | - |
| Flow Monitor Alert | Abnormal flow warning | - |
| Water Usage Alert | Excessive usage warning | - |
| Leak Detector Alert | Water leak warning | - |
| Service Reminder | Maintenance reminder | - |

### System Status
| Sensor | Description | Unit |
|--------|-------------|------|
| Online Status | Device connectivity | - |
| WiFi Signal Strength | Signal strength | dBm |
| Signal Quality | WiFi signal bars | Count |
| Days in Operation | System operation time | Days |
| Power Outage Count | Number of power failures | Count |
| Service Due | Months until service | Months |

## Troubleshooting

### Common Issues

1. **Cannot Connect Error**
   - Check your internet connection
   - Verify your HydroLink credentials
   - Ensure the HydroLink service is operational

2. **Authentication Failed**
   - Double-check your email and password
   - Try logging out and back in to the HydroLink app
   - Reset your HydroLink password if needed

3. **No Data Updates**
   - Check your device's connection to HydroLink
   - Verify the integration is properly configured
   - Restart Home Assistant

### Debug Logging

To enable debug logging for the integration:

1. Add the following to your `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.hydrolink: debug
```
2. Restart Home Assistant
3. Check the logs for detailed information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version History

### Version 1.0.0 (October 2, 2025)
- Initial HACS-compatible release
- Complete restructure for HACS compatibility
- Updated to MIT license
- Added comprehensive testing setup
- Improved documentation and translations
- Added proper branding assets
- Configured CI/CD with GitHub Actions
- Updated minimum Home Assistant version to 2024.10.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to EcoWater for providing the HydroLink platform
- Based on the original [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status) project

## Trademark Legal Notice

This project is not affiliated with, endorsed by, or connected to EcoWater Systems LLC. EcoWater, HydroLink, and any related logos are trademarks of EcoWater Systems LLC. These trademarks are used for reference only.
- Thanks to the Home Assistant community for their support and feedback
