# Pynance - Integrated Financial Management System

"""
Pynance is an integrated system combining five powerful applications:
- PyBudget: Expense tracker and budget management
- Calculator: Advanced calculator with comprehensive mathematical operations
- Pytasker: Task management application with Flask backend
- FileOrganizer: File organization tool with duplicate detection and date-based organization
- PyBot: Chatbot for financial assistance and general queries
"""

from .calculator import Calculator
from .file_organizer.file_organizer.main import main as organizer_main
from .PyBot import app as chatbot_app
from .pybudget import Budget, Expense, generate_report
from .Pytasker.app import app as task_app
from .shared.logging import setup_logging

__all__ = [
    "Budget",
    "Expense",
    "generate_report",
    "Calculator",
    "task_app",
    "chatbot_app",
    "organizer_main",
    "setup_logging",
]
