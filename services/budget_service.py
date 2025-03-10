from models.budget import Budget

def add_budget(category, amount, month, year):
    """Create and save a new budget"""
    budget = Budget(category, amount, month, year)
    budget.save()
    return budget

def get_all_budgets():
    """Get all budgets from database"""
    return Budget.get_all()

def get_budget_by_id(budget_id):
    """Get a specific budget by its ID"""
    return Budget.get_by_id(budget_id)

def delete_budget(budget_id):
    """Delete a budget by its ID"""
    budget = Budget.get_by_id(budget_id)
    if budget:
        budget.delete()
        return True
    return False

def update_budget(budget_id, category, amount, month, year):
    """Update an existing budget"""
    budget = Budget.get_by_id(budget_id)
    if budget:
        budget.category = category
        budget.amount = amount
        budget.month = month
        budget.year = year
        budget.save()
        return True
    return False