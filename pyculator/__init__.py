# pyculator/__init__.py

"""
pyculator: A Python-based calculator module.

This module provides functionality for performing mathematical operations.
"""

from .calculator import Calculator
from .operations import add, divide, multiply, subtract

__all__ = ["Calculator", "add", "subtract", "multiply", "divide"]
