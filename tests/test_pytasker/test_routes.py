"""
Test suite for Pytasker routes.

To run these tests:
1. Make sure you're in the repository root directory
2. Run: pytest tests/test_pytasker/ -v
3. Or run all tests: pytest

Note: The .env file in Pytasker/ provides the SECRET_KEY for testing.
"""

import os
import sys
from unittest.mock import patch

import pytest

# Add the Pytasker directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Pytasker"))
)

import sys

sys.path.insert(0, "/media/cipherjon/HDD/Repo/Pynance/Pytasker")
from app import app, db
from app.models import Task


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_home_route(client):
    with patch("app.routes.render_template", return_value="Mocked Template"):
        response = client.get("/")
        assert response.status_code == 200


def test_add_task_route(client):
    response = client.post(
        "/add", data={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 302  # Redirect status code

    # Verify the task was added
    with app.app_context():
        task = Task.query.filter_by(title="Test Task").first()
        assert task is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"


def test_edit_task_route(client):
    # Add a task first
    with app.app_context():
        task = Task(title="Original Task", description="Original Description")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Edit the task
    response = client.post(
        "/edit",
        data={
            "id": task_id,
            "title": "Updated Task",
            "description": "Updated Description",
        },
    )
    assert response.status_code == 302  # Redirect status code

    # Verify the task was updated
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"


def test_api_tasks_route(client):
    # Test GET request
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json == {"tasks": []}

    # Test POST request
    response = client.post(
        "/api/tasks", json={"title": "API Task", "description": "API Description"}
    )
    assert response.status_code == 201
    assert response.json["title"] == "API Task"
    assert response.json["description"] == "API Description"


def test_delete_task_route(client):
    # Add a task first
    with app.app_context():
        task = Task(title="Task to Delete", description="Delete Description")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Delete the task
    response = client.delete(
        f"/api/tasks/{task_id}", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 204

    # Verify the task was deleted
    with app.app_context():
        deleted_task = Task.query.get(task_id)
        assert deleted_task is None
