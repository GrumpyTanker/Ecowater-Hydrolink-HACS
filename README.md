# EcoWater HydroLink Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/workflows/Validate/badge.svg)](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/actions)
[![HA Core Version](https://img.shields.io/badge/Home%20Assistant-2024.10.0-blue.svg)](https://www.home-assistant.io)
[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org)
[![Test Coverage](https://img.shields.io/badge/Coverage-58%25-yellow.svg)](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Home Assistant integration for EcoWater's HydroLink connected water softeners. Monitor your water softener's performance, water usage, salt levels, and more directly in Home Assistant.

This integration is a HACS-compatible adaptation of the original [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status) project, enhanced with improved data organization, real-time updates via WebSocket, comprehensive error handling, and extensive test coverage.

## ✨ Features

- **Real-time monitoring** of your EcoWater water softener with WebSocket updates
- **Comprehensive sensor coverage** with 8 distinct categories
- **Service integration** for triggering manual regeneration cycles
- **Robust error handling** with automatic reconnection
- **Extensive test coverage** (58% with 55+ comprehensive tests)
- **HACS compatibility** for easy installation and updates
- **Modern async architecture** optimized for Home Assistant 2024.10.0+

## 📋 Prerequisites

- Home Assistant 2024.10.0 or newer  
- Python 3.12+ (for local development and testing)
- EcoWater HydroLink account with active connected device
- Stable internet connection for WebSocket communication

## 🚀 Installation

### HACS Installation (Recommended)

1. **Install HACS** if you haven't already
2. **Add this repository** to HACS:
   - Go to HACS → Integrations
   - Click the three dots (⋮) in the top right
   - Select "Custom repositories"
   - Add `https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS`
   - Category: Integration
3. **Install the integration**:
   - Search for "EcoWater HydroLink" in HACS
   - Click Install
   - Restart Home Assistant
4. **Configure the integration**:
   - Go to Settings → Devices & Services
   - Click "+ ADD INTEGRATION"
   - Search for "EcoWater HydroLink"
   - Enter your HydroLink credentials when prompted

### Manual Installation

1. **Download the latest release** from the [GitHub repository](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/releases)
2. **Extract and copy** the `custom_components/hydrolink` directory to your Home Assistant's `custom_components` directory
3. **Restart Home Assistant**
4. **Add the integration** via Settings → Devices & Services → Add Integration

## ⚙️ Configuration

The integration uses a simple configuration flow:

1. **Navigate to integrations**: Settings → Devices & Services
2. **Add integration**: Click "Add Integration" 
3. **Search for HydroLink**: Type "EcoWater HydroLink" or "HydroLink"
4. **Enter credentials**: Provide your HydroLink email and password
5. **Complete setup**: Click "Submit" and the integration will automatically discover your devices

### Configuration Options

- **Email**: Your EcoWater HydroLink account email
- **Password**: Your EcoWater HydroLink account password
- **Automatic Updates**: Data refreshes every 30 seconds via WebSocket
- **Device Discovery**: Automatically detects all connected HydroLink devices

## 🌊 Available Sensors

The integration provides comprehensive monitoring across 8 categories with 30+ sensors:

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

## 🔧 Services

### `hydrolink.trigger_regeneration`

Manually trigger a regeneration cycle on your water softener.

**Parameters:**
- `device_id` (required): The device ID of your water softener

**Example usage:**
```yaml
service: hydrolink.trigger_regeneration
data:
  device_id: "your_device_id_here"
```

## 🛠️ Troubleshooting

### Common Issues

#### 🚫 Cannot Connect Error
- **Check internet connection**: Ensure stable connection to EcoWater servers
- **Verify credentials**: Double-check email/password in HydroLink app
- **Service status**: Check if HydroLink service is operational
- **Firewall**: Ensure WebSocket connections (WSS) are allowed

#### 🔐 Authentication Failed  
- **Password reset**: Try resetting your HydroLink password
- **App login**: Test credentials in the official HydroLink mobile app
- **Account status**: Verify your HydroLink account is active
- **Special characters**: Ensure password doesn't contain problematic characters

#### 📊 No Data Updates
- **Device connectivity**: Check device connection in HydroLink app
- **Integration reload**: Reload the integration in Home Assistant
- **WebSocket issues**: Check logs for WebSocket connection errors
- **Device status**: Ensure your water softener is online and communicating

#### ⚡ Frequent Disconnections
- **Network stability**: Check for intermittent internet issues  
- **Router settings**: Verify WebSocket traffic isn't being blocked
- **Distance/signal**: Ensure water softener has good WiFi signal
- **Power issues**: Check for power interruptions to the device

### Advanced Debugging

#### Enable Debug Logging

Add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.hydrolink: debug
    custom_components.hydrolink.api: debug
    custom_components.hydrolink.coordinator: debug
```

#### Check Integration Health

1. **Go to**: Settings → Devices & Services → EcoWater HydroLink
2. **View device**: Click on your water softener device  
3. **Check entities**: Verify all sensors are available and updating
4. **Review diagnostics**: Look for error states or unknown values

#### Log Analysis

Common log messages and their meanings:

- `"HydroLink login successful"`: Authentication working properly
- `"WebSocket connection established"`: Real-time updates active  
- `"Authentication expired"`: Credentials need refresh
- `"Connection timeout"`: Network or service connectivity issues
- `"Device data updated"`: Successful data refresh from API

## 🧪 Development & Testing

This integration includes comprehensive test coverage:

- **55+ test cases** covering all major functionality
- **58% code coverage** with focus on critical paths
- **API testing** with mocked responses and error scenarios  
- **Configuration flow testing** for setup validation
- **Coordinator testing** for data update reliability
- **Service testing** for regeneration trigger functionality

### Running Tests Locally

```bash
# Install development dependencies
pip install -r requirements_test.txt

# Run all tests with coverage
python -m pytest tests/ --cov=custom_components --cov-report=term-missing

# Run specific test categories
python -m pytest tests/test_api.py -v
python -m pytest tests/test_config_flow.py -v
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with appropriate tests
4. **Run the test suite**: `python -m pytest tests/`
5. **Update documentation** as needed
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Guidelines

- Follow [Home Assistant development standards](https://developers.home-assistant.io/)
- Maintain or improve test coverage
- Update documentation for new features
- Use type hints and proper docstrings
- Follow existing code style and patterns

## 📚 Version History

### Version 1.1.0 (October 3, 2025) 🎉
#### 🐛 **Bug Fixes & Stability**
- **Fixed HACS validation issues**: Resolved CI/CD pipeline issues
- **Resolved CI/CD pipeline**: Fixed GitHub Actions workflow with Python 3.12+ compatibility  
- **Socket blocking fixes**: Improved test reliability with proper request mocking
- **API interface corrections**: Fixed method naming and response structure handling

#### ✨ **Enhancements**
- **Enhanced test coverage**: Expanded from 22 to 55+ comprehensive tests (58% coverage)
- **Improved error handling**: Better exception management and user feedback
- **Updated Python compatibility**: Full support for Python 3.12+ and Home Assistant 2024.10.0+

#### 🧹 **Maintenance**  
- **Repository cleanup**: Removed build artifacts, cache files, and unused assets
- **Documentation improvements**: Comprehensive README updates with troubleshooting guides
- **Code quality**: Enhanced type hints, docstrings, and inline documentation
- **CI/CD optimization**: Streamlined testing and validation workflows

#### 🔧 **Technical Improvements**
- **Device constructor fixes**: Proper dataclass instantiation with keyword arguments
- **WebSocket stability**: Better connection management and error recovery
- **Test infrastructure**: Comprehensive API, coordinator, and service testing
- **Coverage goals**: Achieved sustainable 58% test coverage with quality focus

### Version 1.0.0 (October 2, 2025) 🚀
#### 🎯 **Initial HACS Release**
- **Complete HACS compatibility**: Full restructure for Home Assistant Community Store
- **Modern architecture**: Async-first design optimized for HA 2024.10.0+
- **License update**: Migrated to MIT License for better compatibility
- **Professional testing**: Comprehensive test setup with pytest and coverage reporting

#### 📦 **Core Features**
- **Multi-sensor support**: 30+ sensors across 8 categories for complete monitoring
- **Real-time updates**: WebSocket integration for live data streaming  
- **Service integration**: Manual regeneration trigger capability
- **Robust error handling**: Graceful failure management and recovery
- **Device discovery**: Automatic detection of connected HydroLink devices

#### 🎨 **User Experience**
- **Improved documentation**: Installation guides, troubleshooting, and examples
- **Internationalization**: English translations with extensible i18n framework
- **Configuration flow**: User-friendly setup process with validation

#### 🔧 **Technical Foundation**
- **GitHub Actions CI/CD**: Automated testing, HACS validation, and quality checks
- **Type safety**: Comprehensive type hints throughout the codebase
- **Modern dependencies**: Updated for current Home Assistant ecosystem
- **Code organization**: Clean separation of concerns and modular design

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### How to Contribute
- **Report Bugs**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml)
- **Suggest Features**: Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml)
- **Submit Code**: Fork the repo and create a pull request
- **Improve Docs**: Documentation improvements are always appreciated

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **EcoWater Systems**: For providing the HydroLink platform and API access
- **Home Assistant Community**: For their continuous support, feedback, and development standards
- **Original Project**: Based on the foundational work of [Hydrolink-Home-Status](https://github.com/GrumpyTanker/Hydrolink-Home-Status)
- **Contributors**: All developers who have contributed code, testing, and documentation improvements
- **HACS Team**: For providing the platform that makes community integrations accessible

## ⚠️ Legal & Trademark Notice

**This project is not affiliated with, endorsed by, or connected to EcoWater Systems LLC.**

- **EcoWater**, **HydroLink**, and related logos are trademarks of EcoWater Systems LLC
- These trademarks are used for reference and identification purposes only
- This integration is an independent, community-driven project
- Use of trademarks falls under fair use for descriptive and compatibility purposes
- No endorsement by EcoWater Systems LLC is implied or claimed

---

## 🔗 Quick Links

### For Users
- [**Report Issues**](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/issues/new?template=bug_report.yml) - Report bugs using our bug report template
- [**Request Features**](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/issues/new?template=feature_request.yml) - Suggest new features or improvements
- [**View Releases**](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/releases) - See what's new in each version
- [**Changelog**](CHANGELOG.md) - Detailed version history
- [**HACS Documentation**](https://hacs.xyz/) - Learn more about HACS

### For Contributors
- [**Contributing Guidelines**](CONTRIBUTING.md) - How to contribute to this project
- [**Code of Conduct**](CODE_OF_CONDUCT.md) - Our community standards
- [**Security Policy**](SECURITY.md) - How to report security vulnerabilities
- [**Development Guide**](https://developers.home-assistant.io/) - Home Assistant development resources

**⭐ If this integration helps you monitor your water softener, please consider giving it a star on GitHub!**
