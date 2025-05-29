from datetime import datetime
from typing import Optional, Dict, Any
import re

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_expense_name(name: str) -> str:
    """Validate expense name."""
    if not name or not isinstance(name, str):
        raise ValidationError("Name must be a non-empty string")
    
    name = name.strip()
    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters long")
    if len(name) > 100:
        raise ValidationError("Name must not exceed 100 characters")
    
    # Remove any potentially harmful characters
    name = re.sub(r'[<>]', '', name)
    return name

def validate_amount(amount: Any) -> float:
    """Validate expense amount."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a valid number")
    
    if amount <= 0:
        raise ValidationError("Amount must be greater than 0")
    if amount > 1000000:  # Reasonable upper limit
        raise ValidationError("Amount exceeds maximum allowed value")
    
    return round(amount, 2)

def validate_category(category: Optional[str]) -> str:
    """Validate expense category."""
    if not category:
        return "Uncategorized"
    
    category = category.strip().lower()
    valid_categories = {'food', 'transportation', 'housing', 'entertainment', 'other', 'uncategorized'}
    
    if category not in valid_categories:
        raise ValidationError(f"Category must be one of: {', '.join(valid_categories)}")
    
    return category

def validate_date(date_str: Optional[str]) -> str:
    """Validate date string."""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if date > datetime.now():
            raise ValidationError("Date cannot be in the future")
        return date.strftime('%Y-%m-%d')
    except ValueError:
        raise ValidationError("Date must be in YYYY-MM-DD format")

def validate_expense_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate complete expense data."""
    if not isinstance(data, dict):
        raise ValidationError("Invalid data format")
    
    validated = {}
    
    # Required fields
    if 'name' not in data:
        raise ValidationError("Name is required")
    validated['name'] = validate_expense_name(data['name'])
    
    if 'amount' not in data:
        raise ValidationError("Amount is required")
    validated['amount'] = validate_amount(data['amount'])
    
    # Optional fields
    validated['category'] = validate_category(data.get('category'))
    validated['date'] = validate_date(data.get('date'))
    
    return validated 