import pytest
from flask import Flask
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from PyBot import User, app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = "test-secret-key"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_home_route_redirect(client):
    response = client.get("/")
    assert response.status_code == 302


def test_register_route(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_login_route(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_logout_route(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_chat_route_unauthorized(client):
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 302


def test_register_user(client):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login_user(client):
    # Register a user first
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
        follow_redirects=True,
    )

    # Login the user
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_chat_route_authorized(client):
    # Register and login a user
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
        follow_redirects=True,
    )

    client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"},
        follow_redirects=True,
    )

    # Test the chat route
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json
