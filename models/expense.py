import sqlite3
from datetime import datetime
from config.config import DATABASE_PATH

class Expense:
    def __init__(self, name, amount, category='Uncategorized', date=None):
        self.name = name
        self.amount = amount
        self.category = category
        self.date = date or datetime.today().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    # Database connection pool to reuse connections
    _connection_pool = None

    @classmethod
    def _get_connection(cls):
        """Get a database connection from the pool"""
        if not cls._connection_pool:
            cls._connection_pool = sqlite3.connect(DATABASE_PATH,
                                                 check_same_thread=False,
                                                 timeout=10)
        return cls._connection_pool

    @classmethod
    def create_table(cls):
        """Initialize database schema safely without data loss"""
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL DEFAULT 'Uncategorized',
                    date DATE NOT NULL DEFAULT CURRENT_DATE
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()