"""Main Execution block"""

from flask import Flask, request, send_from_directory, jsonify
import os
from services.expense_service import add_expense, delete_expense, get_expenses

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/expenses', methods=['POST'])
def api_add_expense():
    data = request.json
    name = data['name']
    amount = data['amount']
    category = data.get('category', 'Uncategorized')  # Optional category with default
    expense = add_expense(name, amount, category)
    # Convert Expense object to a dictionary
    expense_dict = {
        'name': expense.name,
        'amount': expense.amount,
        'category': expense.category
    }
    return jsonify(expense_dict), 201

@app.route('/api/expenses', methods=['GET'])
def api_get_expenses():
    expenses = get_expenses()
    return jsonify(expenses)  # Already returns a list of dicts, no change needed

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def api_delete_expense(expense_id):
    success = delete_expense(expense_id)
    if success:
        return jsonify({'message': 'Expense deleted successfully'}), 200
    return jsonify({'error': 'Expense not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)