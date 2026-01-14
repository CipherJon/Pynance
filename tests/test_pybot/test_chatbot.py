import pytest

from PyBot.bot.chatbot import Chatbot


@pytest.fixture
def chatbot():
    return Chatbot()


def test_chatbot_initialization(chatbot):
    assert chatbot is not None
    assert chatbot.extension_manager is not None
    assert chatbot.preprocessor is not None
    assert chatbot.intents is not None
    assert chatbot.model is not None
    assert chatbot.response_handler is not None


def test_chatbot_get_response(chatbot):
    response = chatbot.get_response("Hello")
    assert response is not None
    assert isinstance(response, str)


def test_chatbot_greeting(chatbot):
    response = chatbot.get_response("Hello")
    assert "Hello" in response or "Hi" in response


def test_chatbot_farewell(chatbot):
    response = chatbot.get_response("Goodbye")
    assert "Goodbye" in response or "Bye" in response


def test_chatbot_unknown(chatbot):
    response = chatbot.get_response("Random text")
    assert "I'm sorry, I don't understand" in response


def test_chatbot_budget_help(chatbot):
    response = chatbot.get_response("How do I create a budget?")
    assert "budget" in response.lower() or "PyBudget" in response


def test_chatbot_calculator_help(chatbot):
    response = chatbot.get_response("How do I use the calculator?")
    assert "calculator" in response.lower() or "Calculator" in response


def test_chatbot_task_help(chatbot):
    response = chatbot.get_response("How do I manage tasks?")
    assert "task" in response.lower() or "Pytasker" in response


def test_chatbot_file_organizer_help(chatbot):
    response = chatbot.get_response("How do I organize my files?")
    assert "file" in response.lower() or "FileOrganizer" in response
