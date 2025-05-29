from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Migrate
migrate = Migrate()

def init_migrations(app):
    """Initialize database migrations with the Flask app."""
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join('data', 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db) 