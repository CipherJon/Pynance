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
            category TEXT DEFAULT 'Uncategorized',
            date DATE NOT NULL DEFAULT CURRENT_DATE
        )
    ''')

    # Check if the category column exists, add it if not
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'category' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT "Uncategorized"')
    if 'date' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN date DATE DEFAULT CURRENT_DATE')

    # Insert the expense
    expense = Expense(name=name, amount=amount, category=category)
    cursor.execute('''
        INSERT INTO expenses (name, amount, category, date)
        VALUES (?, ?, ?, ?)
    ''', (expense.name, expense.amount, expense.category, expense.date))
    
    expense_id = cursor.lastrowid
    cursor.execute('SELECT id, name, amount, category, date FROM expenses WHERE id = ?', (expense_id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {
        "id": row[0],
        "name": row[1],
        "amount": row[2],
        "category": row[3],
        "date": row[4]
    }

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
    cursor.execute('SELECT id, name, amount, category, date FROM expenses')
    expenses = [{"id": row[0], "name": row[1], "amount": row[2], "category": row[3], "date": row[4]} for row in cursor.fetchall()]
    conn.close()
    return expenses

def update_expense(expense_id, name=None, amount=None, category=None, date=None):
    try:
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if amount is not None:
            updates.append("amount = ?")
            params.append(float(amount))
        if category is not None:
            if category.lower() not in {'food', 'transportation', 'housing', 'entertainment', 'other'}:
                raise ValueError(f"Invalid category: {category}. Must be one of: food, transportation, housing, entertainment, other")
            updates.append("category = ?")
            params.append(category.lower())
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        
        if not updates:
            return False  # No fields to update
        
        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount > 0:
            cursor.execute('SELECT id, name, amount, category, date FROM expenses WHERE id = ?', (expense_id,))
            row = cursor.fetchone()
            return {
                "id": row[0],
                "name": row[1],
                "amount": row[2],
                "category": row[3],
                "date": row[4]
            }
        return None
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        return False
    finally:
        if conn:
            conn.close()