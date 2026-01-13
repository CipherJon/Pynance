# pybudget/expense.py

"""
Expense module for tracking individual expenses.
"""


class Expense:
    """
    A class to represent an expense.

    Attributes:
        description (str): A description of the expense.
        amount (float): The amount of the expense.
        category (str): The category of the expense.
    """

    def __init__(self, description: str, amount: float, category: str):
        """
        Initialize an Expense instance.

        Args:
            description (str): A description of the expense.
            amount (float): The amount of the expense.
            category (str): The category of the expense.
        """
        self.description = description
        self.amount = amount
        self.category = category

    def __str__(self):
        """
        Return a string representation of the expense.

        Returns:
            str: A string representation of the expense.
        """
        return f"Expense(description='{self.description}', amount={self.amount}, category='{self.category}')"
