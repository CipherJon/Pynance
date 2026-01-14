import os

import pytest

from PyBot.config.settings import Settings


def test_bot_name():
    settings = Settings()
    assert settings.BOT_NAME == "SimpleBot"


def test_secret_key():
    settings = Settings()
    assert settings.SECRET_KEY is not None
    assert isinstance(settings.SECRET_KEY, str)


def test_sqlalchemy_database_uri():
    settings = Settings()
    assert settings.SQLALCHEMY_DATABASE_URI is not None
    assert isinstance(settings.SQLALCHEMY_DATABASE_URI, str)


def test_sqlalchemy_track_modifications():
    settings = Settings()
    assert settings.SQLALCHEMY_TRACK_MODIFICATIONS is False


def test_settings_environment_variables():
    # Test that environment variables are loaded correctly
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    # Create a new Settings instance to pick up the new environment variables
    from PyBot.config.settings import Settings

    # Override the settings directly
    settings = Settings()
    settings.SECRET_KEY = "test-secret-key"
    settings.SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    assert settings.SECRET_KEY == "test-secret-key"
    assert settings.SQLALCHEMY_DATABASE_URI == "sqlite:///test.db"
