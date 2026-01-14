# main.py

"""
Main entry point for the merged pybudget, pyculator, pytasker, and file_organizer project.
"""

from file_organizer.file_organizer.main import main as organizer_main
from pybudget import Budget, Expense, generate_report
from pyculator import Calculator
from Pytasker.app import app as task_app
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

    # Demonstrate Pytasker functionality
    print("\n=== Pytasker Demo ===")
    print("Starting Pytasker application...")
    print("You can access the task manager at http://localhost:5000")
    print("Run 'flask run' in the Pytasker directory to start the task manager.")

    print("\n=== File Organizer Demo ===")
    print("Running file organizer demo...")
    print("This would organize files in the default directory (~/Downloads)")
    print("To run the actual organizer, use: python pynance.py organizer")


if __name__ == "__main__":
    main()
