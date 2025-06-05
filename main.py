"""Main Execution block"""

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
import logging
from services.expense_service import add_expense, delete_expense, get_expenses, update_expense
from services.auth_service import register_user, login_user, get_user_by_id, update_user, AuthenticationError
from utils.validators import ValidationError, validate_date
from utils.backup import backup_database, restore_from_backup, list_backups
from config.database import init_db
from config.cache import init_cache, cache
from config.migrations import init_migrations, db
from config.monitoring import init_monitoring, metrics
from models.expense import Expense
from models.user import User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='frontend')

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change in production
jwt = JWTManager(app)

# Initialize extensions
init_cache(app)
init_migrations(app)
init_db()  # Initialize the database

# Error handlers
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(Exception)
def handle_generic_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    return jsonify({"error": "An unexpected error occurred"}), 500

# Routes
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/expenses', methods=['POST'])
@limiter.limit("10 per minute")
def api_add_expense():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        expense = add_expense(
            name=data['name'],
            amount=data['amount'],
            category=data.get('category', 'Uncategorized')
        )
        return jsonify(expense), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        return jsonify({"error": "Failed to add expense"}), 500

@app.route('/api/expenses', methods=['GET'])
@limiter.limit("30 per minute")
def api_get_expenses():
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 100)  # Limit max items per page
        category = request.args.get('category')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        search = request.args.get('search')

        # Validate dates if provided
        if start_date:
            start_date = validate_date(start_date)
        if end_date:
            end_date = validate_date(end_date)

        # Get expenses with pagination and filtering
        expenses, total_count = get_expenses(
            page=page,
            per_page=per_page,
            category=category,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
            search=search
        )

        # Calculate pagination metadata
        total_pages = (total_count + per_page - 1) // per_page

        return jsonify({
            'expenses': expenses,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error fetching expenses: {e}")
        return jsonify({"error": "Failed to fetch expenses"}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@limiter.limit("10 per minute")
def api_delete_expense(expense_id):
    try:
        success = delete_expense(expense_id)
        if success:
            return jsonify({"message": "Expense deleted successfully"}), 200
        return jsonify({"error": "Expense not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        return jsonify({"error": "Failed to delete expense"}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@limiter.limit("10 per minute")
def api_update_expense(expense_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        updated = update_expense(expense_id, **data)
        if updated:
            return jsonify(updated), 200
        return jsonify({"error": "Expense not found"}), 404
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating expense: {e}")
        return jsonify({"error": "Failed to update expense"}), 500

# Backup endpoints
@app.route('/api/backup', methods=['POST'])
@limiter.limit("5 per hour")
def api_create_backup():
    """Create a new database backup."""
    try:
        success = backup_database()
        if success:
            return jsonify({"message": "Backup created successfully"}), 200
        return jsonify({"error": "Failed to create backup"}), 500
    except Exception as e:
        logger.error(f"Backup creation failed: {e}")
        return jsonify({"error": "Failed to create backup"}), 500

@app.route('/api/backup', methods=['GET'])
@limiter.limit("30 per minute")
def api_list_backups():
    """List all available backups."""
    try:
        backups = list_backups()
        return jsonify({"backups": backups})
    except Exception as e:
        logger.error(f"Failed to list backups: {e}")
        return jsonify({"error": "Failed to list backups"}), 500

@app.route('/api/backup/<path:filename>', methods=['POST'])
@limiter.limit("5 per hour")
def api_restore_backup(filename):
    """Restore database from a backup file."""
    try:
        backup_file = os.path.join('data', 'backups', filename)
        success = restore_from_backup(backup_file)
        if success:
            # Clear cache after restore
            cache.clear()
            return jsonify({"message": "Backup restored successfully"}), 200
        return jsonify({"error": "Failed to restore backup"}), 500
    except FileNotFoundError:
        return jsonify({"error": "Backup file not found"}), 404
    except Exception as e:
        logger.error(f"Backup restore failed: {e}")
        return jsonify({"error": "Failed to restore backup"}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit: 5 requests per minute
def api_register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        result = register_user(data['username'], data['email'], data['password'])
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'message': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit: 5 requests per minute
def api_login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        result = login_user(data['email'], data['password'])
        return jsonify(result), 200
    except AuthenticationError as e:
        return jsonify({'message': str(e)}), 401
    except ValidationError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'message': 'Login failed'}), 500

if __name__ == '__main__':
    # Start the application
    app.run(debug=True)