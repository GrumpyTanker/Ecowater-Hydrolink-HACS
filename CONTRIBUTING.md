# Contributing to EcoWater HydroLink Integration

First off, thank you for considering contributing to the EcoWater HydroLink integration! It's people like you that make this integration better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible using our [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml).

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml) and provide as much detail as possible.

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Ensure the test suite passes** by running `pytest`
5. **Update documentation** if you've changed APIs or functionality
6. **Write a clear commit message** describing your changes
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Home Assistant 2024.10.0 or newer (for testing)
- Git

### Setting Up Your Development Environment

1. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Ecowater-Hydrolink-HACS.git
   cd Ecowater-Hydrolink-HACS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements_test.txt
   ```

3. **Run tests to ensure everything works:**
   ```bash
   pytest tests/
   ```

### Project Structure

```
Ecowater-Hydrolink-HACS/
├── custom_components/hydrolink/  # Main integration code
│   ├── __init__.py               # Integration setup
│   ├── api.py                    # HydroLink API interface
│   ├── config_flow.py            # Configuration flow
│   ├── coordinator.py            # Data update coordinator
│   ├── sensor.py                 # Sensor entities
│   ├── services.py               # Service definitions
│   ├── const.py                  # Constants
│   ├── manifest.json             # Integration manifest
│   └── translations/             # Translation files
├── tests/                        # Test suite
├── discovery/                    # API discovery tools
└── docs/                         # Documentation
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://github.com/psf/black) for code formatting
- Use [Pylint](https://www.pylint.org/) for linting
- Add type hints to all functions and methods
- Write docstrings for all public functions, classes, and methods

### Code Quality

Run these commands before submitting:

```bash
# Format code
black custom_components/hydrolink tests

# Lint code
pylint custom_components/hydrolink

# Run tests with coverage
pytest tests/ --cov=custom_components/hydrolink --cov-report=term-missing
```

### Testing

- Write tests for all new functionality
- Maintain or improve test coverage (currently 58%)
- Use pytest for testing
- Mock external API calls using pytest fixtures

Example test structure:
```python
import pytest
from custom_components.hydrolink.api import HydroLinkApi

@pytest.mark.asyncio
async def test_api_functionality(mock_api):
    """Test API functionality."""
    # Your test code here
    pass
```

### Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Keep the first line under 72 characters
- Add detailed description if needed

Examples:
```
Add support for new sensor types
Fix WebSocket reconnection logic
Update documentation for configuration options
```

## Documentation

- Update README.md if you change functionality
- Update info.md for HACS-specific information
- Add docstrings to all new functions and classes
- Update version history in relevant files

## Versioning

We use [Semantic Versioning](https://semver.org/). For the versions available, see the [tags on this repository](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/tags).

## Release Process

1. Update version in `manifest.json`
2. Update version in `__init__.py`
3. Update `README.md` with changes
4. Create a new tag and release on GitHub
5. HACS will automatically pick up the new version

## Questions?

Feel free to open an issue with the "question" label or reach out through the [Home Assistant Community Forum](https://community.home-assistant.io/).

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to EcoWater HydroLink! 🎉
