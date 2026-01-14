#!/usr/bin/env python3

"""
Pynance - Unified entry point for the integrated financial management system.

This script provides a command-line interface to access all components of Pynance:
- PyBudget: Expense tracking and budget management
- PyCalculator: Advanced calculator functionality
- Pytasker: Task management system
- FileOrganizer: File organization tool
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


def run_organizer_with_args(args):
    """Run the File Organizer with specific arguments."""
    print("\n=== File Organizer ===")

    import logging
    import sys
    from pathlib import Path

    from file_organizer.file_organizer.config import LOG_CONFIG
    from file_organizer.file_organizer.organizer import organize_files

    # Validate LOG_CONFIG dictionary
    required_keys = ["level", "format", "file"]
    for key in required_keys:
        if key not in LOG_CONFIG:
            raise ValueError(f"LOG_CONFIG is missing required key: {key}")

    # Ensure the log file directory exists and is writable
    log_file_path = Path(LOG_CONFIG["file"])
    if not log_file_path.parent.exists():
        try:
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(
                f"WARNING: Could not create log directory: {e}. Falling back to default location."
            )
            log_file_path = Path.home() / "file_organizer.log"

    # Check if the log file is writable
    try:
        with open(log_file_path, "a") as f:
            pass
    except Exception as e:
        print(
            f"WARNING: Could not write to log file: {e}. Falling back to default location."
        )
        log_file_path = Path.home() / "file_organizer.log"

    # Set up logging based on verbose flag
    level = logging.DEBUG if args.verbose else getattr(logging, LOG_CONFIG["level"])
    logging.basicConfig(
        level=level,
        format=LOG_CONFIG["format"],
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Call organize_files with the specified arguments
    base_dir = args.directory if args.directory else None
    results = organize_files(base_dir, args.workers)

    # Print results
    if results["success"]:
        print("\nSuccessfully processed files:")
        for msg in results["success"]:
            print(f"✓ {msg}")

    if results["failed"]:
        print("\nFailed to process files:")
        for msg in results["failed"]:
            print(f"✗ {msg}")


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
  python pynance.py organizer    - Run File Organizer
  python pynance.py all          - Run all demos
        """,
    )

    # Create subparsers for commands that need their own arguments
    subparsers = parser.add_subparsers(dest="command", help="Component to run")

    # Organizer subparser
    organizer_parser = subparsers.add_parser("organizer", help="Run File Organizer")
    organizer_parser.add_argument(
        "--directory",
        "-d",
        type=str,
        help="Directory to organize (default: ~/Downloads)",
    )
    organizer_parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Number of worker threads (default: 4)",
    )
    organizer_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    # Other commands don't need additional arguments
    subparsers.add_parser("budget", help="Run PyBudget demo")
    subparsers.add_parser("calculator", help="Run PyCalculator demo")
    subparsers.add_parser("tasker", help="Start Pytasker web application")
    subparsers.add_parser("all", help="Run all demos")

    args = parser.parse_args()

    if args.command == "budget":
        run_budget_demo()
    elif args.command == "calculator":
        run_calculator_demo()
    elif args.command == "tasker":
        run_tasker()
    elif args.command == "organizer":
        # Call organizer with its specific arguments
        run_organizer_with_args(args)
    elif args.command == "all":
        run_budget_demo()
        run_calculator_demo()
        print("\nTo run Pytasker, use: python pynance.py tasker")
        print("To run File Organizer, use: python pynance.py organizer")


if __name__ == "__main__":
    main()
