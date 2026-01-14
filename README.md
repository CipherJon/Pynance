# Pynance - Integrated Financial Management System

## Overview

Pynance is an integrated system combining four powerful applications:
- **PyBudget**: Expense tracker and budget management
- **PyCalculator**: Advanced calculator with comprehensive mathematical operations
- **Pytasker**: Task management application with Flask backend
- **FileOrganizer**: File organization tool with duplicate detection and date-based organization

## Features

### PyBudget
- Track expenses and manage budgets
- Generate detailed budget reports
- Categorize expenses for better financial tracking

### PyCalculator
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Advanced mathematical operations (power, square root, percentage, modulo, absolute value)
- Calculation history and clear screen functionality
- Comprehensive error handling

### FileOrganizer
- Organize files into categories based on file extensions
- Date-based organization (monthly/quarterly)
- Duplicate file detection and handling
- Parallel processing for better performance
- Comprehensive logging
- Safe file operations with backup support
- Command-line interface with various options

### Pytasker
- Full-stack task management application
- Flask backend with SQLAlchemy database
- RESTful API for task management
- CORS support for frontend-backend communication

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Pynance
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Main Application

To see all functionalities in action:
```bash
python main.py
```

To run the file organizer:
```bash
python pynance.py organizer
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

### FileOrganizer Usage

```bash
# Run the file organizer
python pynance.py organizer

# With options:
python pynance.py organizer --directory /path/to/directory --workers 8 --verbose
```

### Pytasker Usage

To run the Pytasker task management application:

1. Navigate to the Pytasker directory:
   ```bash
   cd Pytasker
   ```

2. Run the Flask application:
   ```bash
   flask run
   ```

3. Open your browser to http://localhost:5000 to access the task manager

### Unified CLI

Pynance provides a unified CLI to access all components:

```bash
python pynance.py [budget|calculator|tasker|all]
```

- `budget`: Run PyBudget demo
- `calculator`: Run PyCalculator demo
- `tasker`: Start Pytasker web application
- `organizer`: Run File Organizer
- `all`: Run all demos

## Project Structure

```
Pynance/
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
├── file_organizer/
│   ├── file_organizer/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── organizer.py
│   │   └── utils.py
│   ├── scripts/
│   └── tests/
├── Pytasker/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── config.py
│   └── manage.py
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
├── pynance.py
├── README.md
├── requirements.txt
└── setup.py
```

## Testing

Run the tests to ensure everything is working correctly:
```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License.
