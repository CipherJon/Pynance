# pybudget/budget.py

"""
Budget module for managing budgets and tracking expenses.
"""


class Budget:
    """
    A class to represent a budget.

    Attributes:
        name (str): The name of the budget.
        amount (float): The total amount allocated for the budget.
        expenses (list): A list of expenses associated with the budget.
    """

    def __init__(self, name: str, amount: float):
        """
        Initialize a Budget instance.

        Args:
            name (str): The name of the budget.
            amount (float): The total amount allocated for the budget.
        """
        self.name = name
        self.amount = amount
        self.expenses = []

    def add_expense(self, expense):
        """
        Add an expense to the budget.

        Args:
            expense: An Expense object to add to the budget.
        """
        self.expenses.append(expense)

    def get_remaining_amount(self) -> float:
        """
        Calculate the remaining amount in the budget.

        Returns:
            float: The remaining amount in the budget.
        """
        total_expenses = sum(expense.amount for expense in self.expenses)
        return self.amount - total_expenses

    def __str__(self):
        """
        Return a string representation of the budget.

        Returns:
            str: A string representation of the budget.
        """
        return f"Budget(name='{self.name}', amount={self.amount}, remaining={self.get_remaining_amount()})"
