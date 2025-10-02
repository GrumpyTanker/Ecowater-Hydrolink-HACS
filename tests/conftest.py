# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Test Configuration

Provides shared test configuration and fixtures for all HydroLink tests.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic test configuration
  
- 0.2.0 (2025-10-02)
  * Added socket disabling
  * Improved test isolation

License: Apache License 2.0
See LICENSE file in the project root for full license information.
import pytest
from pytest_socket import disable_socket

@pytest.fixture(autouse=True)
def disable_socket_for_tests():
    """Disable socket usage for all tests."""
    disable_socket()