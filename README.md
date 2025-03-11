# Expense Tracker

A comprehensive expense tracking application with both command-line interface (CLI) and web interface for managing personal finances, budgets, and generating detailed reports.

## Features

### Core Functionality
- Add, view, edit, and delete expenses with descriptions, amounts, categories, and dates
- Income tracking and categorization
- Transaction history with filtering and sorting

### Budget Management
- Create and manage multiple budgets
- Set monthly budget limits per category
- Real-time budget progress tracking
- Alerts when approaching budget limits

### Reporting & Analytics
- Generate detailed financial reports (daily, weekly, monthly)
- Visualize spending patterns with charts and graphs
- Export reports to CSV/PDF formats
- Year-over-year spending comparisons

### Data Management
- Secure SQLite database storage
- Data import/export functionality
- Multi-user support with individual profiles
- Cloud sync capabilities (optional)

### Interface Options
- Intuitive command-line interface (CLI)
- Responsive web interface with dashboard
- Dark/Light theme support
- Mobile-friendly design

## Requirements

- Python 3.10+
- SQLite 3.32+
- Modern web browser (for web interface)
- Node.js v18+ (optional for frontend development)

## Installation

### CLI Application
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/expense_tracker.git
    ```
2. Navigate to the project directory:
    ```sh
    cd expense_tracker
    ```
3. Install Python dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Web Interface
1. Ensure you have a modern web browser (Chrome, Firefox, or Edge)
2. Open `frontend/index.html` in your browser
3. (Optional) For local development:
    ```sh
    cd frontend
    npm install  # If package.json exists
    ```

## Usage

### Command-Line Interface
```sh
python main.py
```
- Follow the interactive menu to manage expenses and budgets
- Example commands:
  - Add expense: `add "Groceries" 75.50 Food`
  - Generate report: `report monthly 2023-10`

### Web Interface
1. Launch the web interface by opening `frontend/index.html`
2. Use the dashboard to:
   - View financial overview
   - Add/edit transactions
   - Configure budget limits
   - Generate interactive reports

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
