import pytest
from app import app, db
from models.user import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register_user(client):
    """Test user registration."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['user']['username'] == 'testuser'
    assert data['user']['email'] == 'test@example.com'

def test_register_duplicate_username(client):
    """Test registration with duplicate username."""
    # First registration
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test1@example.com',
        'password': 'password123'
    })
    
    # Second registration with same username
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'Username already exists' in response.get_json()['message']

def test_register_duplicate_email(client):
    """Test registration with duplicate email."""
    # First registration
    client.post('/api/auth/register', json={
        'username': 'testuser1',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Second registration with same email
    response = client.post('/api/auth/register', json={
        'username': 'testuser2',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'Email already exists' in response.get_json()['message']

def test_login_success(client):
    """Test successful login."""
    # Register user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['user']['username'] == 'testuser'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'Invalid username or password' in response.get_json()['message']

def test_protected_route(client):
    """Test accessing protected route."""
    # Register and login
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']
    
    # Access protected route
    response = client.get('/api/expenses', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200

def test_protected_route_no_token(client):
    """Test accessing protected route without token."""
    response = client.get('/api/expenses')
    assert response.status_code == 401

def test_protected_route_invalid_token(client):
    """Test accessing protected route with invalid token."""
    response = client.get('/api/expenses', headers={
        'Authorization': 'Bearer invalid-token'
    })
    assert response.status_code == 401 