"""
Utility functions for the calculator module.
"""

from typing import Any


def format_number(number: float) -> str:
    """
    Format a number as a string with two decimal places.

    Args:
        number (float): The number to format

    Returns:
        str: The formatted number as a string
    """
    return f"{number:.2f}"


def validate_number(value: Any) -> bool:
    """
    Validate if the provided value is a valid number.

    Args:
        value (Any): The value to validate

    Returns:
        bool: True if the value is a valid number, False otherwise
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
