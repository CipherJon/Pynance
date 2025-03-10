import sqlite3
from models.expense import Expense

def add_expense(name, amount, category='Uncategorized'):
    # Connect to the database
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    # Create the expenses table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'Uncategorized'
        )
    ''')

    # Check if the category column exists, add it if not
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'category' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT "Uncategorized"')

    # Insert the expense
    expense = Expense(name=name, amount=amount, category=category)
    cursor.execute('''
        INSERT INTO expenses (name, amount, category)
        VALUES (?, ?, ?)
    ''', (expense.name, expense.amount, expense.category))
    
    conn.commit()
    conn.close()
    return expense

def get_expenses():
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, amount, category FROM expenses')
    expenses = [{"name": row[0], "amount": row[1], "category": row[2]} for row in cursor.fetchall()]
    conn.close()
    return expenses