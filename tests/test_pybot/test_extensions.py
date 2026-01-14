import pytest

from PyBot.bot.core.extensions import Extension, ExtensionManager


class MockExtension(Extension):
    def process_message(self, message: str, context: dict) -> dict:
        context["mock_processed"] = True
        return context


@pytest.fixture
def extension_manager():
    return ExtensionManager()


def test_extension_manager_initialization(extension_manager):
    assert extension_manager is not None
    assert extension_manager.extensions == []


def test_extension_manager_register(extension_manager):
    mock_extension = MockExtension()
    extension_manager.register(mock_extension)
    assert len(extension_manager.extensions) == 1
    assert isinstance(extension_manager.extensions[0], MockExtension)


def test_extension_manager_process_message(extension_manager):
    mock_extension = MockExtension()
    extension_manager.register(mock_extension)
    context = {}
    processed_context = extension_manager.process_message("test message", context)
    assert processed_context is not None
    assert "mock_processed" in processed_context
    assert processed_context["mock_processed"] is True
