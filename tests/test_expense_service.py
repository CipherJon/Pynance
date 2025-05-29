import pytest
from services.expense_service import add_expense, get_expenses, update_expense, delete_expense
from utils.validators import ValidationError

def test_add_expense():
    # Test valid expense
    expense = add_expense("Test Expense", 100.50, "food")
    assert expense["name"] == "Test Expense"
    assert expense["amount"] == 100.50
    assert expense["category"] == "food"
    
    # Test invalid amount
    with pytest.raises(ValidationError):
        add_expense("Test Expense", -100, "food")
    
    # Test invalid category
    with pytest.raises(ValidationError):
        add_expense("Test Expense", 100, "invalid_category")

def test_get_expenses():
    # Add test expenses
    add_expense("Expense 1", 100, "food")
    add_expense("Expense 2", 200, "transportation")
    
    # Get all expenses
    expenses = get_expenses()
    assert len(expenses) >= 2
    assert any(e["name"] == "Expense 1" for e in expenses)
    assert any(e["name"] == "Expense 2" for e in expenses)

def test_update_expense():
    # Add test expense
    expense = add_expense("Original Name", 100, "food")
    expense_id = expense["id"]
    
    # Update expense
    updated = update_expense(expense_id, name="Updated Name", amount=150)
    assert updated["name"] == "Updated Name"
    assert updated["amount"] == 150
    
    # Test invalid update
    with pytest.raises(ValidationError):
        update_expense(expense_id, amount=-100)

def test_delete_expense():
    # Add test expense
    expense = add_expense("To Delete", 100, "food")
    expense_id = expense["id"]
    
    # Delete expense
    assert delete_expense(expense_id) is True
    
    # Verify deletion
    expenses = get_expenses()
    assert not any(e["id"] == expense_id for e in expenses)
    
    # Test deleting non-existent expense
    assert delete_expense(999999) is False 