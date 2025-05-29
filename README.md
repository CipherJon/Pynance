# PyBudget - Personal Budget Management System

A Flask-based web application for managing personal expenses and tracking budgets.

## Features

- Add, update, and delete expenses
- Categorize expenses
- Track spending over time
- RESTful API endpoints
- Input validation and error handling
- Rate limiting and security measures
- CORS support for frontend integration

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PyBudget.git
cd PyBudget
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python main.py
```

2. Access the application at `http://localhost:5000`

## API Endpoints

### GET /api/expenses
- Returns a list of all expenses
- Rate limit: 30 requests per minute

### POST /api/expenses
- Creates a new expense
- Required fields: name, amount
- Optional fields: category
- Rate limit: 10 requests per minute

### PUT /api/expenses/<id>
- Updates an existing expense
- Optional fields: name, amount, category, date
- Rate limit: 10 requests per minute

### DELETE /api/expenses/<id>
- Deletes an expense
- Rate limit: 10 requests per minute

## Testing

Run the test suite:
```bash
pytest
```

## Project Structure

```
PyBudget/
├── config/             # Configuration files
├── data/              # Database files
├── frontend/          # Frontend static files
├── models/            # Data models
├── services/          # Business logic
├── tests/             # Test files
├── utils/             # Utility functions
├── views/             # View templates
├── main.py           # Application entry point
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Security Features

- Input validation for all user inputs
- Rate limiting to prevent abuse
- CORS configuration for frontend security
- SQL injection prevention through parameterized queries
- Error handling and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

