import sqlite3

class Budget:
    def __init__(self, category, amount, month, year, id=None):
        self.id = id
        self.category = category
        self.amount = amount
        self.month = month
        self.year = year

    def to_dict(self):
        return {
            "category": self.category,
            "amount": self.amount,
            "month": self.month,
            "year": self.year
        }

    @staticmethod
    def create_table():
        """Initialize database table if it doesn't exist"""
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        """Save budget to database"""
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO budgets (category, amount, month, year)
            VALUES (?, ?, ?, ?)
        ''', (self.category, self.amount, self.month, self.year))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        """Get all budgets from database"""
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM budgets')
        budgets = [
            cls(
                category=row[1],
                amount=row[2],
                month=row[3],
                year=row[4],
                id=row[0]
            ) for row in cursor.fetchall()
        ]
        conn.close()
        return budgets

    @classmethod
    def get_by_id(cls, budget_id):
        """Get a single budget by ID"""
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM budgets WHERE id = ?', (budget_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(
                category=row[1],
                amount=row[2],
                month=row[3],
                year=row[4],
                id=row[0]
            )
        return None

    def delete(self):
        """Delete this budget from the database"""
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM budgets WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()