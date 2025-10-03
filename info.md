# EcoWater HydroLink Integration

Monitor and control your EcoWater water softener system through the HydroLink cloud service in Home Assistant. Get real-time updates on water usage, salt levels, system performance, and more.

**Version 1.1.0** - Enhanced stability, comprehensive testing, and HACS compliance

## ✨ Features

- **Real-time monitoring** via WebSocket connection with automatic reconnection
- **Service integration** for manual regeneration control
- **Comprehensive sensor coverage** across 8 categories with 30+ sensors:
  - 🌊 Water Usage (Current Flow, Daily Usage, Peak Flow)
  - 🧂 Salt Management (Level, Days Remaining, Usage Stats)  
  - ⚙️ System Performance (Capacity, Hardness, Treatment)
  - 🔄 Regeneration Status and Control
  - 🚨 Alert Monitoring (Salt, Flow, Leaks, Errors)
  - 📶 Signal and Connection Quality
  - 🔧 Maintenance Tracking and Reminders
  - 📊 Historical Data and Statistics

## 🚀 What's New in v1.1.0

- **Enhanced reliability** with 58% test coverage (55+ comprehensive tests)
- **Fixed HACS validation** and CI/CD pipeline issues
- **Improved error handling** and WebSocket stability  
- **Updated compatibility** for Home Assistant 2024.10.0+ and Python 3.12+
- **Repository cleanup** and comprehensive documentation updates

## ⚙️ Quick Setup

1. **Install via HACS**: Search for "EcoWater HydroLink" in HACS integrations
2. **Restart Home Assistant** after installation
3. **Add Integration**: Settings → Devices & Services → Add Integration
4. **Search for "HydroLink"** and select the integration
5. **Enter credentials**: Your HydroLink email and password
6. **Enjoy monitoring**: All sensors will be automatically discovered

## 🛠️ Requirements

- Home Assistant 2024.10.0 or newer
- Active EcoWater HydroLink account with connected device
- Stable internet connection for WebSocket communication

## 🆘 Support

- **Issues & Bugs**: [GitHub Issues](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/discussions)
- **Community Support**: [Home Assistant Community Forum](https://community.home-assistant.io/)
- **Documentation**: [Full README](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS#readme)

**⭐ Please star the repository if this integration helps you!**