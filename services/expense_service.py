import logging
from typing import List, Dict, Optional, Any, Tuple
from config.database import get_db_connection
from utils.validators import validate_expense_data, ValidationError

logger = logging.getLogger(__name__)

def add_expense(name: str, amount: float, category: str = 'Uncategorized') -> Dict[str, Any]:
    """Add a new expense to the database."""
    try:
        # Validate input data
        data = validate_expense_data({
            'name': name,
            'amount': amount,
            'category': category
        })
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (name, amount, category, date)
                VALUES (?, ?, ?, ?)
            ''', (data['name'], data['amount'], data['category'], data['date']))
            
            expense_id = cursor.lastrowid
            conn.commit()
            
            # Fetch and return the created expense
            cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
            row = cursor.fetchone()
            return dict(row)
            
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        raise

def delete_expense(expense_id: int) -> bool:
    """Delete an expense from the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        raise

def get_expenses(
    page: int = 1,
    per_page: int = 10,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """Get expenses with pagination and filtering."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build query conditions
            conditions = []
            params = []
            
            if category:
                conditions.append("category = ?")
                params.append(category.lower())
            
            if start_date:
                conditions.append("date >= ?")
                params.append(start_date)
            
            if end_date:
                conditions.append("date <= ?")
                params.append(end_date)
            
            if min_amount is not None:
                conditions.append("amount >= ?")
                params.append(min_amount)
            
            if max_amount is not None:
                conditions.append("amount <= ?")
                params.append(max_amount)
            
            if search:
                conditions.append("(name LIKE ? OR category LIKE ?)")
                search_term = f"%{search}%"
                params.extend([search_term, search_term])
            
            # Build the query
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            query = f"SELECT * FROM expenses WHERE {where_clause} ORDER BY date DESC"
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM expenses WHERE {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Add pagination
            query += " LIMIT ? OFFSET ?"
            params.extend([per_page, (page - 1) * per_page])
            
            # Execute query
            cursor.execute(query, params)
            expenses = [dict(row) for row in cursor.fetchall()]
            
            return expenses, total_count
            
    except Exception as e:
        logger.error(f"Error fetching expenses: {e}")
        raise

def update_expense(expense_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    """Update an existing expense in the database."""
    try:
        # Validate update data
        data = validate_expense_data(kwargs)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build update query dynamically based on provided fields
            updates = []
            params = []
            for key, value in data.items():
                updates.append(f"{key} = ?")
                params.append(value)
            
            if not updates:
                return None
            
            # Add updated_at timestamp
            updates.append("updated_at = CURRENT_TIMESTAMP")
            
            # Add expense_id to params
            params.append(expense_id)
            
            # Execute update
            query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            if cursor.rowcount > 0:
                conn.commit()
                # Fetch and return updated expense
                cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
            
            return None
            
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error updating expense: {e}")
        raise