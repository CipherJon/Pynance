import sqlite3
from services.expense_service import add_expense, get_expenses, view_expenses, delete_expense, update_expense
from services.budget_service import add_budget, get_budgets, delete_budget, update_budget
from services.report_service import ReportService
from models.expense import Expense
from models.budget import Budget
from utils.helpers import format_currency
from datetime import datetime

def manage_budgets():
    while True:
        print("\nBudget Management")
        print("1. Add Budget")
        print("2. View Budgets")
        print("3. Delete Budget")
        print("4. Update Budget")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == '1':
            category = input("Enter category: ")
            amount = float(input("Enter monthly budget amount: "))
            month = datetime.now().month
            year = datetime.now().year
            add_budget(category, amount, month, year)
            print("Budget added successfully.")
        elif choice == '2':
            budgets = get_budgets()
            print("\nBudgets:")
            for budget in budgets:
                print(f"ID: {budget[0]}, Category: {budget[1]}, Amount: {format_currency(budget[2])}, Month/Year: {budget[3]}/{budget[4]}")
        elif choice == '3':
            budget_id = int(input("Enter budget ID to delete: "))
            delete_budget(budget_id)
            print("Budget deleted successfully.")
        elif choice == '4':
            budget_id = int(input("Enter budget ID to update: "))
            category = input("Enter new category: ")
            amount = float(input("Enter new amount: "))
            month = int(input("Enter new month (1-12): "))
            year = int(input("Enter new year: "))
            update_budget(budget_id, category, amount, month, year)
            print("Budget updated successfully.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def get_current_budget(category):
    current_month = datetime.now().month
    current_year = datetime.now().year
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount) FROM budgets
        WHERE category = ? AND month = ? AND year = ?
    ''', (category, current_month, current_year))
    result = cursor.fetchone()
    conn.close()
from services.budget_service import add_budget, get_all_budgets, delete_budget

def manage_budgets():
    while True:
        print("\nBudget Management")
        print("1. Add Budget")
        print("2. View All Budgets")
        print("3. Delete Budget")
        print("4. Return to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year: "))
            add_budget(category, amount, month, year)
            print("Budget added successfully!")
        elif choice == '2':
            budgets = get_all_budgets()
            for budget in budgets:
                print(f"ID: {budget.id} | {budget.category}: ${budget.amount} | {budget.month}/{budget.year}")
        elif choice == '3':
            budget_id = int(input("Enter budget ID to delete: "))
            if delete_budget(budget_id):
                print("Budget deleted successfully!")
            else:
                print("Budget not found!")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def get_current_spending(category):
    current_month = datetime.now().month
    current_year = datetime.now().year
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount) FROM expenses
        WHERE category = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    ''', (category, f"{current_month:02d}", current_year))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0

def main_menu():
    Expense.create_table()
    Budget.create_table()
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. Manage Budgets")
        print("6. Generate Reports")
        print("7. Exit")

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
            category = input("Enter new category (optional): ")
            update_expense(expense_id, description, amount, date, category)
            print("Expense updated successfully.")
        elif choice == '5':
            manage_budgets()
        elif choice == '6':
            report = ReportService.generate_full_report()
            print("\nFinancial Report:")
            print(f"Generated at: {report['generated_at']}")
            
            print("\nCategory Breakdown:")
            for category, amount in report['category_report']['categories'].items():
                print(f"- {category}: {format_currency(amount)}")
            print(f"Total: {format_currency(report['category_report']['total'])}")
            
            print("\nMonthly Trends:")
            for month, amount in report['time_report']['monthly'].items():
                print(f"- {month}: {format_currency(amount)}")
                
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")