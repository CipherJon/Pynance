from models.expense import Expense

def add_expense(name, amount):
    expense = Expense(name=name, amount=amount)
    # Here you should add the expense to the database
    # For simplicity, we're just returning the created expense
    return expense

def get_expenses():
    # Here you should fetch the expenses from the database
    # For simplicity, we're returning a static list
    return [
        {"name": "Groceries", "amount": 50},
        {"name": "Rent", "amount": 500}
    ]