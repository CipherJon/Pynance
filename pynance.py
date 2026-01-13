#!/usr/bin/env python3

"""
Pynance - Unified entry point for the integrated financial management system.

This script provides a command-line interface to access all components of Pynance:
- PyBudget: Expense tracking and budget management
- PyCalculator: Advanced calculator functionality
- Pytasker: Task management system
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_budget_demo():
    """Run the PyBudget demo."""
    print("=== PyBudget Demo ===")
    from pybudget import Budget, Expense, generate_report

    budget = Budget("Monthly Budget", 5000.0)
    expense1 = Expense("Groceries", 150.0, "Food")
    expense2 = Expense("Rent", 1200.0, "Housing")
    budget.add_expense(expense1)
    budget.add_expense(expense2)
    print(generate_report(budget))


def run_calculator_demo():
    """Run the PyCalculator demo."""
    print("\n=== PyCalculator Demo ===")
    from pyculator import Calculator

    calculator = Calculator()
    result_add = calculator.add(10, 5)
    result_subtract = calculator.subtract(10, 5)
    result_multiply = calculator.multiply(10, 5)
    result_divide = calculator.divide(10, 5)

    print(f"Addition: 10 + 5 = {result_add}")
    print(f"Subtraction: 10 - 5 = {result_subtract}")
    print(f"Multiplication: 10 * 5 = {result_multiply}")
    print(f"Division: 10 / 5 = {result_divide}")


def run_tasker():
    """Start the Pytasker Flask application."""
    print("\n=== Starting Pytasker ===")
    print("Starting Flask application...")
    print("Access the task manager at http://localhost:5000")
    print("Press Ctrl+C to stop the server")

    # Change to Pytasker directory
    pytasker_dir = Path(__file__).parent / "Pytasker"
    os.chdir(pytasker_dir)

    # Set Flask environment variables
    os.environ["FLASK_APP"] = "manage.py"
    os.environ["FLASK_ENV"] = "development"

    # Run Flask application
    try:
        subprocess.run(["flask", "run"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Pytasker: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nPytasker stopped by user")
        sys.exit(0)


def main():
    """Main entry point for Pynance CLI."""
    parser = argparse.ArgumentParser(
        description="Pynance - Integrated Financial Management System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pynance.py budget       - Run PyBudget demo
  python pynance.py calculator   - Run PyCalculator demo
  python pynance.py tasker       - Start Pytasker web application
  python pynance.py all          - Run all demos
        """,
    )

    parser.add_argument(
        "command",
        choices=["budget", "calculator", "tasker", "all"],
        help="Component to run",
    )

    args = parser.parse_args()

    if args.command == "budget":
        run_budget_demo()
    elif args.command == "calculator":
        run_calculator_demo()
    elif args.command == "tasker":
        run_tasker()
    elif args.command == "all":
        run_budget_demo()
        run_calculator_demo()
        print("\nTo run Pytasker, use: python pynance.py tasker")


if __name__ == "__main__":
    main()
