# EcoWater HydroLink Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/workflows/Validate/badge.svg)](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/YOUR_REPO_ID/maintainability)](https://codeclimate.com/github/GrumpyTanker/Ecowater-Hydrolink-HACS)
[![Coverage](https://codecov.io/gh/GrumpyTanker/Ecowater-Hydrolink-HACS/branch/main/graph/badge.svg)](https://codecov.io/gh/GrumpyTanker/Ecowater-Hydrolink-HACS)

A Home Assistant integration for EcoWater's HydroLink connected water softeners. Monitor your water softener's performance, water usage, salt levels, and more directly in Home Assistant.

This integration is a HACS-compatible adaptation of the original [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status) project, enhanced with improved data organization, real-time updates via WebSocket, and comprehensive error handling.

## Features

- Real-time monitoring of your EcoWater water softener
- Automatic data updates every 5 minutes
- Multiple sensors for comprehensive monitoring:
  - Water Usage (Today, Yesterday, Average)
  - Salt Level and Days Remaining
  - Water Pressure (Inlet/Outlet)
  - Water Temperature (Inlet/Outlet)
  - Regeneration Status and Schedule
  - System Errors and Connectivity
  - Vacation Mode Status

## Installation

### HACS Installation (Preferred)
1. Ensure you have [HACS](https://hacs.xyz) installed in your Home Assistant instance
2. Search for "EcoWater HydroLink" in HACS
3. Click Install
4. Restart Home Assistant
5. Add the integration via the Home Assistant UI (Configuration -> Devices & Services -> + Add Integration)
6. Search for "EcoWater HydroLink"
7. Enter your HydroLink credentials when prompted
6. Select "Integration" as the category
7. Click "Add"
8. Find "EcoWater HydroLink" in the integration list and install it
9. Restart Home Assistant

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

| Sensor | Description | Unit | Default Enabled |
|--------|-------------|------|-----------------|
| Water Usage Today | Today's water consumption | Gallons | Yes |
| Water Usage Yesterday | Yesterday's water consumption | Gallons | Yes |
| Average Daily Water Usage | Average daily water usage | Gallons | Yes |
| Salt Level | Current salt level | % | Yes |
| Salt Days Remaining | Days until salt needs refilling | Days | Yes |
| Water Flow Rate | Current water flow rate | GPM | Yes |
| Water Hardness | Water hardness level | GPG | Yes |
| Water Pressure | Current water pressure | PSI | Yes |
| Water Temperature | Current water temperature | °F | Yes |
| Regeneration Status | Days until next regeneration | Days | Yes |
| Last Regeneration | Timestamp of last regeneration | - | Yes |
| System Error | Any current system errors | - | Yes |
| Online Status | Device connectivity status | - | Yes |
| Vacation Mode | Vacation mode status | - | Yes |

### Diagnostic Sensors (Hidden by Default)

These sensors are available but hidden by default. They can be enabled in the Home Assistant UI if needed:

| Sensor | Description | Unit |
|--------|-------------|------|
| WiFi Signal Strength | Device WiFi signal strength | dBm |
| Days Since Last Time Loss | Days since last power outage | Days |
| Power Outage Count | Number of power outages | Count |
| Total Untreated Water | Total untreated water used | Gallons |
| Rock Salt Removed | Total hardness removed | lbs |
| Salt Efficiency | Grains of hardness removed per lb of salt | Grains/lb |
| Error Code | Current error code | - |
| Error Alert Status | Error alert flag | - |
| Leak Alert Status | Water leak detection status | - |
| Flow Monitor Alert | Excessive flow alert status | - |
| Last Service Date | Date of last service | - |
| Software Version | Device firmware version | - |

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

### Version 0.3.1 (October 2, 2025)
- Fixed config flow error handling
- Improved exception handling and propagation
- Enhanced test infrastructure reliability
- Added comprehensive error state management
- Fixed async executor job handling

### Version 0.3.0
- Added comprehensive documentation of all sensors
- Added diagnostic sensors section
- Improved data cleaning and organization
- Enhanced example data with complete attribute descriptions
- Added discovery tools for development

### Version 0.2.0
- Added WebSocket support for real-time updates
- Added HACS compatibility
- Improved error handling and logging
- Added type hints and dataclass models
- Enhanced data organization and cleaning
- Added example data for development

### Version 0.1.0
- Initial release based on Hydrolink-Home-Status
- Basic API implementation
- Device data retrieval

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to EcoWater for providing the HydroLink platform
- Based on the original [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status) project

## Trademark Legal Notice

This project is not affiliated with, endorsed by, or connected to EcoWater Systems LLC. EcoWater, HydroLink, and any related logos are trademarks of EcoWater Systems LLC. These trademarks are used for reference only.
- Thanks to the Home Assistant community for their support and feedback
