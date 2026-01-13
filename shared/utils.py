# shared/utils.py

"""
Utility functions for shared use across the project.
"""


def validate_input(input_value, input_type):
    """
    Validate that the input is of the specified type.

    Args:
        input_value: The input value to validate.
        input_type: The expected type of the input.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    return isinstance(input_value, input_type)


def format_string(input_string: str) -> str:
    """
    Format a string to ensure it is clean and properly formatted.

    Args:
        input_string (str): The string to format.

    Returns:
        str: The formatted string.
    """
    return input_string.strip()
