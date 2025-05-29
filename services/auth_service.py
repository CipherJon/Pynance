import logging
from typing import Optional, Dict, Any
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
from config.migrations import db
from utils.validators import ValidationError

logger = logging.getLogger(__name__)

def register_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """Register a new user."""
    try:
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            raise ValidationError("Username already exists")
        if User.query.filter_by(email=email).first():
            raise ValidationError("Email already exists")
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error registering user: {e}")
        raise

def login_user(username: str, password: str) -> Dict[str, Any]:
    """Login a user."""
    try:
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            raise ValidationError("Invalid username or password")
        
        if not user.is_active:
            raise ValidationError("User account is disabled")
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise

def get_user_by_id(user_id: int) -> Optional[User]:
    """Get user by ID."""
    try:
        return User.query.get(user_id)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise

def update_user(user_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    """Update user information."""
    try:
        user = User.query.get(user_id)
        if not user:
            return None
        
        if 'username' in kwargs:
            existing = User.query.filter_by(username=kwargs['username']).first()
            if existing and existing.id != user_id:
                raise ValidationError("Username already exists")
            user.username = kwargs['username']
        
        if 'email' in kwargs:
            existing = User.query.filter_by(email=kwargs['email']).first()
            if existing and existing.id != user_id:
                raise ValidationError("Email already exists")
            user.email = kwargs['email']
        
        if 'password' in kwargs:
            user.set_password(kwargs['password'])
        
        db.session.commit()
        return user.to_dict()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user: {e}")
        raise 