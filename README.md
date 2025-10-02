# EcoWater HydroLink Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/github/license/GrumpyTanker/hydrolink-hacs)](LICENSE)

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
1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: https://github.com/GrumpyTanker/hydrolink-hacs
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

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to EcoWater for providing the HydroLink platform
- Thanks to the Home Assistant community for their support and feedback
