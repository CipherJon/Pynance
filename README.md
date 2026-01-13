<<<<<<< HEAD
# Merged Project: PyBudget and PyCalculator

## Overview

This project merges two Python applications, `pybudget` and `pyculator`, into a cohesive system. `pybudget` is an expense tracker, and `pyculator` is a calculator. The merged project allows users to manage budgets and perform calculations seamlessly.

## Features

- **PyBudget**: Track expenses, manage budgets, and generate reports.
- **PyCalculator**: Perform basic mathematical operations (addition, subtraction, multiplication, division).
- **Shared Utilities**: Common utilities and configurations for both modules.
=======
# Advanced Calculator

A feature-rich command-line calculator with support for various mathematical operations, calculation history, and comprehensive error handling.

## Features

- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Advanced mathematical operations:
  - Power/exponentiation
  - Square root
  - Percentage calculations
  - Modulo operation
  - Absolute value
- Calculation history
- Clear screen functionality
- Comprehensive error handling:
  - Input validation
  - NaN detection and handling
  - Division by zero protection
  - Graceful handling of keyboard interrupts (Ctrl+C, Ctrl+D)
- Type hints and documentation
- Unit tests with pytest
>>>>>>> origin/main

## Installation

1. Clone the repository:
<<<<<<< HEAD
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
=======
```bash
git clone https://github.com/yourusername/calculator.git
cd calculator
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the calculator:
```bash
python -m calculator.main
```

### Available Operations

1. Add
2. Subtract
3. Multiply
4. Divide
5. Power
6. Square Root
7. Percentage
8. Modulo
9. Absolute Value

### Additional Commands

- `h`: Show calculation history
- `c`: Clear screen
- `q`: Quit calculator

### Error Handling

The calculator includes comprehensive error handling:
- Invalid numeric inputs are rejected with clear error messages
- NaN (Not a Number) values are detected and rejected
- Division by zero is prevented
- Keyboard interrupts (Ctrl+C, Ctrl+D) are handled gracefully
- All operations include proper input validation

## Development

### Running Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=calculator
```

### Code Style

The project follows PEP 8 style guidelines. You can check the code style using:
```bash
flake8 calculator tests
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
>>>>>>> origin/main
