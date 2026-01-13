# main.py

"""
Main entry point for the merged pybudget and pyculator project.
"""

from pybudget import Budget, Expense, generate_report
from pyculator import Calculator
from shared.logging import setup_logging


def main():
    """
    Main function to demonstrate the merged functionality.
    """
    setup_logging()

    # Demonstrate pybudget functionality
    print("=== PyBudget Demo ===")
    budget = Budget("Monthly Budget", 5000.0)
    expense1 = Expense("Groceries", 150.0, "Food")
    expense2 = Expense("Rent", 1200.0, "Housing")
    budget.add_expense(expense1)
    budget.add_expense(expense2)
    print(generate_report(budget))

    # Demonstrate pyculator functionality
    print("\n=== PyCalculator Demo ===")
    calculator = Calculator()
    result_add = calculator.add(10, 5)
    result_subtract = calculator.subtract(10, 5)
    result_multiply = calculator.multiply(10, 5)
    result_divide = calculator.divide(10, 5)
    print(f"Addition: 10 + 5 = {result_add}")
    print(f"Subtraction: 10 - 5 = {result_subtract}")
    print(f"Multiplication: 10 * 5 = {result_multiply}")
    print(f"Division: 10 / 5 = {result_divide}")


if __name__ == "__main__":
    main()
