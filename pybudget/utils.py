# pybudget/utils.py

"""
Utility functions for the pybudget module.
"""


def validate_amount(amount: float) -> bool:
    """
    Validate that the amount is a positive number.

    Args:
        amount (float): The amount to validate.

    Returns:
        bool: True if the amount is valid, False otherwise.
    """
    return amount > 0


def format_currency(amount: float) -> str:
    """
    Format a number as a currency string.

    Args:
        amount (float): The amount to format.

    Returns:
        str: The formatted currency string.
    """
    return f"${amount:.2f}"
