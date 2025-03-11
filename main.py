"""Main Execution block"""

from flask import Flask, request, send_from_directory, jsonify
import os
from services.expense_service import add_expense, delete_expense, get_expenses, update_expense

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
    expense_data = add_expense(name, amount, category)
    return jsonify({
        'id': expense_data['id'],
        'name': expense_data['name'],
        'amount': expense_data['amount'],
        'category': expense_data['category'],
        'date': expense_data['date']
    }), 201

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

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def api_update_expense(expense_id):
    try:
        data = request.json
        updated = update_expense(
            expense_id,
            name=data.get('name'),
            amount=data.get('amount'),
            category=data.get('category'),
            date=data.get('date')
        )
        if updated:
            return jsonify({
                'id': updated['id'],
                'name': updated['name'],
                'amount': updated['amount'],
                'category': updated['category'],
                'date': updated['date']
            }), 200
        return jsonify({'error': 'Expense not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)