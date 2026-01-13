# tests/test_pybudget/test_reports.py

"""
Unit tests for the reports module in the pybudget module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from pybudget.budget import Budget
from pybudget.expense import Expense
from pybudget.reports import generate_report


class TestReports(unittest.TestCase):
    """
    Test cases for the reports module.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.budget = Budget("Test Budget", 1000.0)
        self.expense1 = Expense("Test Expense 1", 200.0, "Test Category 1")
        self.expense2 = Expense("Test Expense 2", 300.0, "Test Category 2")
        self.budget.add_expense(self.expense1)
        self.budget.add_expense(self.expense2)

    def test_generate_report_with_expenses(self):
        """
        Test generating a report for a budget with expenses.
        """
        report = generate_report(self.budget)
        self.assertIn("Budget Report for 'Test Budget'", report)
        self.assertIn("Total Budget: $1000.00", report)
        self.assertIn("Remaining Budget: $500.00", report)
        self.assertIn("Test Expense 1", report)
        self.assertIn("Test Expense 2", report)

    def test_generate_report_no_expenses(self):
        """
        Test generating a report for a budget with no expenses.
        """
        empty_budget = Budget("Empty Budget", 500.0)
        report = generate_report(empty_budget)
        self.assertIn("Budget Report for 'Empty Budget'", report)
        self.assertIn("Total Budget: $500.00", report)
        self.assertIn("Remaining Budget: $500.00", report)
        self.assertIn("No expenses recorded.", report)


if __name__ == "__main__":
    unittest.main()
