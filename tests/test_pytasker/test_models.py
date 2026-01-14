import os
import sys

import pytest

# Add the Pytasker directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Pytasker"))
)

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


def test_task_creation(client):
    with app.app_context():
        task = Task(title="Test Task", description="Test Description")
        db.session.add(task)
        db.session.commit()

        retrieved_task = Task.query.filter_by(title="Test Task").first()
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Test Description"


def test_task_to_dict(client):
    with app.app_context():
        task = Task(title="Test Task", description="Test Description")
        task_dict = task.to_dict()

        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert "id" in task_dict
