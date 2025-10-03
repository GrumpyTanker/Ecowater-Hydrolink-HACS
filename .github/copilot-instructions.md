# GitHub Copilot Instructions for EcoWater HydroLink Integration

This document provides context and guidelines for GitHub Copilot when working with the EcoWater HydroLink Home Assistant integration.

## Project Overview

This is a custom Home Assistant integration that connects EcoWater HydroLink water softeners to Home Assistant. The integration provides real-time monitoring of water usage, salt levels, system performance, and regeneration status through a WebSocket connection to the HydroLink cloud service.

**Repository**: GrumpyTanker/Ecowater-Hydrolink-HACS  
**Integration Type**: Cloud Polling Hub  
**Domain**: `hydrolink`  
**Version**: 1.1.0  
**License**: MIT

## Architecture

### Core Components

- **`api.py`**: HydroLink cloud API client with authentication and WebSocket communication
- **`coordinator.py`**: Home Assistant data update coordinator for managing API calls and data refresh
- **`config_flow.py`**: Configuration flow for user-friendly setup via UI
- **`sensor.py`**: Sensor platform implementation with 30+ sensors across 8 categories
- **`services.py`**: Service handlers for manual regeneration triggers
- **`const.py`**: Constants and configuration values

### Data Flow

1. User credentials authenticate with HydroLink API
2. WebSocket connection established for real-time updates
3. Coordinator manages periodic data fetches (30-second intervals)
4. Sensors update based on coordinator data
5. Services allow user-triggered actions (e.g., regeneration)

## Development Standards

### Home Assistant Compliance

- Follow [Home Assistant development standards](https://developers.home-assistant.io/)
- Integration type: `hub` (cloud-polling)
- Quality scale: `silver`
- Config flow: Required (no YAML configuration)
- Use `async`/`await` patterns for all I/O operations
- Implement proper error handling and logging
- Use Home Assistant's `DataUpdateCoordinator` for data management

### Code Style

- **Python Version**: 3.12+ required
- **Formatter**: Black (line length 88)
- **Linter**: Ruff + Pylint (configured in `.pylintrc`)
- **Type Hints**: Required for all functions and methods
- **Docstrings**: Use Google-style docstrings for all public functions
- **Pre-commit**: Configured with hooks for code quality

### File Headers

All Python files should include:
```python
# -*- coding: utf-8 -*-
"""
Brief module description

Detailed description of the module's purpose.

Author: GrumpyTanker + AI
Created: [Date]
Updated: [Date]

Changelog:
- Version (Date)
  * Changes

License: MIT
See LICENSE file in the project root for full license information.
"""
```

## Testing Requirements

### Test Coverage

- **Target**: 58% code coverage (current baseline)
- **Test Count**: 55+ comprehensive tests
- **Framework**: pytest with pytest-homeassistant-custom-component

### Test Categories

1. **API Tests** (`test_api.py`): Mock API responses, error scenarios, WebSocket behavior
2. **Config Flow Tests** (`test_config_flow.py`): Setup validation, error handling
3. **Coordinator Tests** (`test_coordinator.py`): Data updates, error recovery
4. **Sensor Tests** (`test_sensor.py`): Sensor creation, state updates
5. **Service Tests** (`test_services.py`): Service calls, validation
6. **Init Tests** (`test_init.py`): Integration setup and unload

### Running Tests

```bash
# Install dependencies
pip install -r requirements_test.txt

# Run all tests with coverage
python -m pytest tests/ --cov=custom_components --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_api.py -v

# Run with specific marker
python -m pytest -m asyncio tests/
```

### Test Fixtures

Located in `tests/conftest.py`:
- `hass`: Mock Home Assistant instance
- `mock_config_entry`: Sample config entry
- `mock_event_loop`: Async event loop for tests
- Socket blocking automatically disabled for test isolation

## Code Patterns

### Sensor Implementation

```python
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfVolume

class HydroLinkSensor(SensorEntity):
    """Base sensor for HydroLink."""
    
    def __init__(self, coordinator, key: str, name: str):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._coordinator.data.get(self._key)
```

### Error Handling

```python
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

try:
    await api.authenticate()
except AuthenticationError as err:
    raise ConfigEntryAuthFailed(f"Authentication failed: {err}") from err
except ConnectionError as err:
    raise ConfigEntryNotReady(f"Connection failed: {err}") from err
```

### Logging

```python
import logging
_LOGGER = logging.getLogger(__name__)

# Use appropriate log levels
_LOGGER.debug("Detailed debug information")
_LOGGER.info("Important status information")
_LOGGER.warning("Recoverable issue")
_LOGGER.error("Error that affects functionality")
```

## Common Tasks

### Adding a New Sensor

1. Define sensor key in `const.py` if needed
2. Add sensor class in `sensor.py` inheriting from `HydroLinkSensor`
3. Set appropriate device class and unit of measurement
4. Update sensor list in `async_setup_entry()`
5. Add test case in `tests/test_sensor.py`
6. Update documentation in README.md

### Modifying API Behavior

1. Update `api.py` with new methods or parameters
2. Update coordinator in `coordinator.py` if data structure changes
3. Add/update tests in `tests/test_api.py`
4. Ensure backward compatibility or increment version
5. Update documentation

### Adding a Service

1. Define service constant in `const.py`
2. Implement service handler in `services.py`
3. Update `services.yaml` with service schema
4. Register service in `async_setup_entry()` in `__init__.py`
5. Add translations in `translations/en.json`
6. Add test in `tests/test_services.py`

## Dependencies

### Runtime Requirements
- `requests>=2.31.0`: HTTP client for API calls
- `websocket-client>=1.7.0`: WebSocket communication
- `voluptuous>=0.13.1`: Schema validation

### Development Requirements
- Home Assistant 2024.10.0+
- pytest and related testing tools
- Code quality tools (black, ruff, pylint, mypy)
- pre-commit hooks

## CI/CD

### GitHub Actions Workflows

- **test.yaml**: Runs pytest suite on Python 3.9, 3.10, 3.11
- **validate.yaml**: Validates manifest and HACS configuration
- **hacs.yaml**: HACS validation
- **hassfest.yaml**: Home Assistant manifest validation

### Pre-commit Hooks

Run before committing:
```bash
pre-commit install
pre-commit run --all-files
```

## Documentation

### User-Facing Documentation

- **README.md**: Installation, configuration, troubleshooting
- **info.md**: HACS display information
- **translations/**: User-facing strings for config flow and services

### Code Documentation

- Inline comments for complex logic only
- Comprehensive docstrings for public APIs
- Type hints for all function parameters and returns

## Common Pitfalls

1. **Async/Await**: Always use `async`/`await` for Home Assistant operations
2. **Blocking Calls**: Don't use blocking I/O; use `hass.async_add_executor_job()` if needed
3. **Data Coordinator**: Always update sensors through coordinator, not direct API calls
4. **Config Entry**: Never modify config entry data directly; use `hass.config_entries.async_update_entry()`
5. **Testing**: Mock all external API calls; never make real network requests in tests
6. **Logging**: Use `_LOGGER` not `print()`; include context in log messages

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [HACS Documentation](https://hacs.xyz/)
- [HydroLink API Documentation](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS)
- [Original Project](https://github.com/GrumpyTanker/Hydrolink-Home-Status)

## Support and Contributions

- **Issues**: [GitHub Issues](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/discussions)
- **Code Owner**: @GrumpyTanker

When contributing:
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run test suite and ensure coverage is maintained
5. Update documentation
6. Submit pull request with clear description
