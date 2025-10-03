# Changelog

All notable changes to the EcoWater HydroLink Integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-03

### Added
- Enhanced test coverage to 58% with 55+ comprehensive tests
- Improved test reliability and socket handling
- GitHub issue templates for bug reports and feature requests
- Security policy (SECURITY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- Comprehensive changelog

### Fixed
- HACS validation issues and CI/CD pipeline
- Device dataclass instantiation and API response handling
- WebSocket connection stability and error recovery
- Socket blocking issues in tests

### Changed
- Updated for Home Assistant 2024.10.0+ compatibility
- Updated for Python 3.12+ compatibility
- Improved error handling throughout the integration
- Enhanced documentation and repository structure

## [1.0.0] - 2025-10-02

### Added
- Initial HACS-compatible release
- Complete restructure for HACS compliance
- Comprehensive testing setup with pytest
- WebSocket support for real-time updates
- Service registration for manual regeneration
- Type hints throughout the codebase
- Translation support (English)
- Professional documentation

### Changed
- Updated to MIT license
- Improved documentation and README
- Enhanced error handling and logging
- Better data organization and cleaning

### Features
- 30+ sensors across 8 categories:
  - Water Usage and Flow monitoring
  - Salt Management tracking
  - System Performance metrics
  - Regeneration Status and Control
  - System Health and Alerts
  - System Status indicators
  - Diagnostic information
  - Historical data tracking
- Real-time WebSocket updates
- Automatic reconnection handling
- Config flow for easy setup
- HACS integration for simple installation

## [0.2.0] - 2025-06-12

### Added
- Service registration for triggering regeneration
- Data update coordinator
- Type hints for better code quality
- Improved error handling

### Changed
- Enhanced API interface
- Better data structure organization

## [0.1.0] - 2025-06-12

### Added
- Initial release
- Basic integration setup
- Config flow implementation
- Device data retrieval
- Sensor platform support
- Basic API implementation based on Hydrolink-Home-Status

[1.1.0]: https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/releases/tag/v1.1.0
[1.0.0]: https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/releases/tag/v1.0.0
[0.2.0]: https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/releases/tag/v0.1.0
