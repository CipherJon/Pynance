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

def delete_expense(expense_id):
    try:
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        return deleted
    except sqlite3.Error as e:
        print(f"Database error during deletion: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_expenses():
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, amount, category FROM expenses')
    expenses = [{"id": row[0], "name": row[1], "amount": row[2], "category": row[3]} for row in cursor.fetchall()]
    conn.close()
    return expenses