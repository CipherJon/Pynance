import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
from config.config import DATABASE_PATH

class ReportService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DATABASE_PATH)

    @classmethod
    def generate_category_report(cls, period_days=30):
        """Generate expense breakdown by category for given period"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=period_days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE date >= ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (start_date,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {
            'period': f'Last {period_days} days',
            'categories': {cat: round(amt, 2) for cat, amt in results},
            'total': round(sum(amt for _, amt in results), 2)
        }

    @classmethod
    def generate_time_period_report(cls):
        """Generate monthly and weekly expense summaries"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Monthly breakdown
        cursor.execute('''
            SELECT strftime('%Y-%m', date), SUM(amount)
            FROM expenses
            GROUP BY strftime('%Y-%m', date)
            ORDER BY date DESC
        ''')
        monthly = cursor.fetchall()
        
        # Weekly breakdown
        cursor.execute('''
            SELECT strftime('%Y-%W', date), SUM(amount)
            FROM expenses
            GROUP BY strftime('%Y-%W', date)
            ORDER BY date DESC
        ''')
        weekly = cursor.fetchall()
        
        conn.close()
        
        return {
            'monthly': {month: round(amt, 2) for month, amt in monthly},
            'weekly': {week: round(amt, 2) for week, amt in weekly}
        }

    @classmethod
    def generate_full_report(cls):
        """Comprehensive report combining all metrics"""
        return {
            'category_report': cls.generate_category_report(),
            'time_report': cls.generate_time_period_report(),
            'generated_at': datetime.now().isoformat()
        }