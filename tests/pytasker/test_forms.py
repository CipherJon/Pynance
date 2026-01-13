import os
import sys

import pytest

# Add the Pytasker directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Pytasker"))
)

from app import app
from app.forms import TaskForm


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            yield client


def test_task_form_validation(client):
    form = TaskForm(title="Test Task", description="Test Description")
    assert form.validate() is True


def test_task_form_empty_title(client):
    form = TaskForm(title="", description="Test Description")
    assert form.validate() is False


def test_task_form_empty_description(client):
    form = TaskForm(title="Test Task", description="")
    assert form.validate() is True


def test_task_form_empty_fields(client):
    form = TaskForm(title="", description="")
    assert form.validate() is False
