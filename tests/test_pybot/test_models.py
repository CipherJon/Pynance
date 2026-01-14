import pytest

from PyBot.config.models import User, db


def test_user_model():
    user = User(username="testuser", email="test@example.com")
    user.set_password("testpassword")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash is not None
    assert user.check_password("testpassword") is True
    assert user.check_password("wrongpassword") is False


def test_user_id():
    user = User(username="testuser", email="test@example.com")
    assert user.id is None
