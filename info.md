# EcoWater HydroLink Integration

This integration allows you to monitor your EcoWater water softener system through the HydroLink cloud service in Home Assistant.

Based on the original [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status) project, enhanced with HACS compatibility, real-time updates, and improved data organization.

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

## Configuration

1. Go to Settings → Devices & Services in Home Assistant
2. Click "Add Integration"
3. Search for "HydroLink"
4. Enter your HydroLink email and password
5. Click "Submit"

## Support

- Report issues on [GitHub](https://github.com/GrumpyTanker/hydrolink-hacs/issues)
- Join the discussion in the [Home Assistant Community](https://community.home-assistant.io/)