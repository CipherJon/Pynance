# Merged Project: PyBudget and PyCalculator

## Overview

This project merges two Python applications, `pybudget` and `pyculator`, into a cohesive system. `pybudget` is an expense tracker, and `pyculator` is a calculator. The merged project allows users to manage budgets and perform calculations seamlessly.

## Features

- **PyBudget**: Track expenses, manage budgets, and generate reports.
- **PyCalculator**: Perform basic mathematical operations (addition, subtraction, multiplication, division).
- **Shared Utilities**: Common utilities and configurations for both modules.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd merged_project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application to see both functionalities in action:
```bash
python main.py
```

### PyBudget Usage

```python
from pybudget import Budget, Expense, generate_report

# Create a budget
budget = Budget("Monthly Budget", 5000.0)

# Add expenses
expense1 = Expense("Groceries", 150.0, "Food")
expense2 = Expense("Rent", 1200.0, "Housing")
budget.add_expense(expense1)
budget.add_expense(expense2)

# Generate a report
print(generate_report(budget))
```

### PyCalculator Usage

```python
from pyculator import Calculator

# Create a calculator instance
calculator = Calculator()

# Perform operations
result_add = calculator.add(10, 5)
result_subtract = calculator.subtract(10, 5)
result_multiply = calculator.multiply(10, 5)
result_divide = calculator.divide(10, 5)

print(f"Addition: 10 + 5 = {result_add}")
print(f"Subtraction: 10 - 5 = {result_subtract}")
print(f"Multiplication: 10 * 5 = {result_multiply}")
print(f"Division: 10 / 5 = {result_divide}")
```

## Project Structure

```
merged_project/
│
├── pybudget/
│   ├── __init__.py
│   ├── budget.py
│   ├── expense.py
│   ├── reports.py
│   └── utils.py
│
├── pyculator/
│   ├── __init__.py
│   ├── calculator.py
│   ├── operations.py
│   └── utils.py
│
├── shared/
│   ├── __init__.py
│   ├── config.py
│   ├── logging.py
│   └── utils.py
│
├── tests/
│   ├── test_pybudget/
│   ├── test_pyculator/
│   └── test_shared/
│
├── main.py
├── README.md
└── requirements.txt
```

## Testing

Run the tests to ensure everything is working correctly:
```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License.
```

Now I will update the `requirements.txt` file to reflect any dependencies used in the project. Based on the code, there are no external dependencies, but I will ensure the file is accurate.