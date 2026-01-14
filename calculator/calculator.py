"""
Calculator class for performing arithmetic operations and maintaining history.
"""


class Calculator:
    """
    A class to perform arithmetic operations and maintain a history of operations.
    """

    def __init__(self):
        """
        Initialize the Calculator with an empty history.
        """
        self.history = []

    def add(self, a: float, b: float) -> float:
        """
        Add two numbers and record the operation in history.

        Args:
            a (float): First number
            b (float): Second number

        Returns:
            float: Sum of a and b
        """
        result = a + b
        self.history.append(f"Added {a} and {b} to get {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """
        Subtract the second number from the first and record the operation in history.

        Args:
            a (float): First number
            b (float): Second number

        Returns:
            float: Difference between a and b
        """
        result = a - b
        self.history.append(f"Subtracted {b} from {a} to get {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers and record the operation in history.

        Args:
            a (float): First number
            b (float): Second number

        Returns:
            float: Product of a and b
        """
        result = a * b
        self.history.append(f"Multiplied {a} and {b} to get {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        """
        Divide the first number by the second and record the operation in history.

        Args:
            a (float): First number
            b (float): Second number

        Returns:
            float: Quotient of a and b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"Divided {a} by {b} to get {result}")
        return result

    def get_history(self) -> list:
        """
        Retrieve the operation history.

        Returns:
            list: List of operation history strings
        """
        return self.history
