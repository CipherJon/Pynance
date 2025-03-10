import sqlite3

class Expense:
    def __init__(self, name, amount, category='Uncategorized'):
        self.name = name
        self.amount = amount
        self.category = category

    def to_dict(self):
        return {"name": self.name, "amount": self.amount, "category": self.category}

    @staticmethod
    def create_table():
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        # Drop existing table to ensure clean schema migration
        cursor.execute('DROP TABLE IF EXISTS expenses')
        
        # Create new table with updated schema
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL DEFAULT 'Uncategorized'
            )
        ''')
        conn.commit()
        conn.close()