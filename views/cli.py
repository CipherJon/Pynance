from services.expense_service import add_expense, get_expenses
from models.expense import Expense
from utils.helpers import format_currency

def main_menu():
    Expense.create_table()
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            category = input("Enter category (optional): ")
            add_expense(description, amount, category)
            print("Expense added successfully.")
        elif choice == '2':
            expenses = view_expenses()
            print("\nExpenses:")
            for expense in expenses:
                print(f"ID: {expense[0]}, Description: {expense[1]}, Amount: {format_currency(expense[2])}, Category: {expense[3]}")
        elif choice == '3':
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)
            print("Expense deleted successfully.")
        elif choice == '4':
            expense_id = int(input("Enter expense ID to update: "))
            description = input("Enter new description: ")
            amount = float(input("Enter new amount: "))
            date = input("Enter new date (YYYY-MM-DD): ")
            update_expense(expense_id, description, amount, date)
            print("Expense updated successfully.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")