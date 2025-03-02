import sqlite3

class Expense:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def to_dict(self):
        return {"name": self.name, "amount": self.amount}

    @staticmethod
    def create_table():
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()