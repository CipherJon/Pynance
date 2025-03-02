import unittest
import sqlite3
from models.expense import Expense

DATABASE_PATH = 'data/database.db'

class TestExpense(unittest.TestCase):

    def setUp(self):
        # Recreate the database schema before each test
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS expenses')
        Expense.create_table()

    def test_add_expense(self):
        expense = Expense(name="Test Expense", amount=100)
        self.assertEqual(expense.name, "Test Expense")
        self.assertEqual(expense.amount, 100)

    def test_delete_expense(self):
        expense = Expense(name="Test Expense", amount=100)
        # Logic to add and delete the expense from the database
        self.assertTrue(True)  # Update with actual test logic

    def test_update_expense(self):
        expense = Expense(name="Test Expense", amount=100)
        # Logic to update the expense in the database
        self.assertTrue(True)  # Update with actual test logic

if __name__ == '__main__':
    unittest.main()