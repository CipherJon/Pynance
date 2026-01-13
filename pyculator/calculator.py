# pyculator/calculator.py

"""
Calculator module for performing mathematical operations.
"""


class Calculator:
    """
    A class to represent a calculator.

    Attributes:
        history (list): A list of operations performed by the calculator.
    """

    def __init__(self):
        """
        Initialize a Calculator instance.
        """
        self.history = []

    def add(self, a: float, b: float) -> float:
        """
        Add two numbers and record the operation in history.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The result of the addition.
        """
        result = a + b
        self.history.append(f"Added {a} and {b} to get {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """
        Subtract two numbers and record the operation in history.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The result of the subtraction.
        """
        result = a - b
        self.history.append(f"Subtracted {b} from {a} to get {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers and record the operation in history.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The result of the multiplication.
        """
        result = a * b
        self.history.append(f"Multiplied {a} and {b} to get {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        """
        Divide two numbers and record the operation in history.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The result of the division.

        Raises:
            ValueError: If the divisor is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"Divided {a} by {b} to get {result}")
        return result

    def get_history(self) -> list:
        """
        Retrieve the history of operations performed by the calculator.

        Returns:
            list: A list of operation history strings.
        """
        return self.history
