# shared/__init__.py

"""
shared: Shared utilities and configurations for the merged project.

This module provides shared functionality used by both pybudget and pyculator.
"""

from .config import SharedConfig
from .logging import setup_logging
from .utils import validate_input

__all__ = ["SharedConfig", "setup_logging", "validate_input"]
