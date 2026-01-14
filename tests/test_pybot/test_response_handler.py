import pytest

from PyBot.bot.chatbot import ResponseHandler


@pytest.fixture
def intents():
    return [
        {
            "tag": "greeting",
            "patterns": ["Hello", "Hi"],
            "responses": ["Hello!", "Hi there!"],
        },
        {
            "tag": "farewell",
            "patterns": ["Goodbye", "Bye"],
            "responses": ["Goodbye!", "See you later!"],
        },
        {
            "tag": "unknown",
            "patterns": ["*", "?", ""],
            "responses": ["I'm sorry, I don't understand."],
        },
    ]


@pytest.fixture
def response_handler(intents):
    return ResponseHandler(intents)


def test_response_handler_initialization(response_handler):
    assert response_handler is not None
    assert response_handler.intents is not None
    assert isinstance(response_handler.intents, list)
    assert len(response_handler.intents) > 0


def test_response_handler_process_message(response_handler):
    context = {"processed_text": "hello", "predicted_intent": "greeting"}
    processed_context = response_handler.process_message("test message", context)
    assert processed_context is not None
    assert "response" in processed_context
    assert isinstance(processed_context["response"], str)


def test_response_handler_unknown_intent(response_handler):
    context = {"processed_text": "unknown", "predicted_intent": "unknown"}
    processed_context = response_handler.process_message("test message", context)
    assert processed_context is not None
    assert "response" in processed_context
    assert "I'm sorry, I don't understand" in processed_context["response"]


def test_response_handler_missing_intent(response_handler):
    context = {"processed_text": "hello", "predicted_intent": "missing_intent"}
    processed_context = response_handler.process_message("test message", context)
    assert processed_context is not None
    assert "response" in processed_context
    assert "I'm sorry, I don't understand" in processed_context["response"]


def test_response_handler_error_handling(response_handler):
    context = {"processed_text": "hello", "predicted_intent": "greeting"}
    # Simulate an error by modifying the intents
    response_handler.intents = None
    processed_context = response_handler.process_message("test message", context)
    assert processed_context is not None
    assert "response" in processed_context
    assert "Error processing request" in processed_context["response"]
