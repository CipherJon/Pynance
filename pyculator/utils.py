# pyculator/utils.py

"""
Utility functions for the pyculator module.
"""


def validate_number(number: float) -> bool:
    """
    Validate that the number is a valid float.

    Args:
        number (float): The number to validate.

    Returns:
        bool: True if the number is valid, False otherwise.
    """
    return isinstance(number, (int, float))


def format_number(number: float) -> str:
    """
    Format a number as a string with two decimal places.

    Args:
        number (float): The number to format.

    Returns:
        str: The formatted number string.
    """
    return f"{number:.2f}"
