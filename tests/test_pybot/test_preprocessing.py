import pytest

from PyBot.bot.core.preprocessing import TextPreprocessor


@pytest.fixture
def preprocessor():
    return TextPreprocessor()


def test_preprocessor_initialization(preprocessor):
    assert preprocessor is not None
    assert preprocessor.lemmatizer is not None
    assert preprocessor.stop_words is not None


def test_preprocessor_preprocess_text(preprocessor):
    text = "Hello, how are you?"
    processed_text = preprocessor.preprocess_text(text)
    assert processed_text is not None
    assert isinstance(processed_text, str)


def test_preprocessor_process_message(preprocessor):
    message = "Hello, how are you?"
    context = {}
    processed_context = preprocessor.process_message(message, context)
    assert processed_context is not None
    assert "processed_text" in processed_context
    assert isinstance(processed_context["processed_text"], str)


def test_preprocessor_lowercase(preprocessor):
    text = "HELLO"
    processed_text = preprocessor.preprocess_text(text)
    assert processed_text == "hello"


def test_preprocessor_remove_stopwords(preprocessor):
    text = "This is a test"
    processed_text = preprocessor.preprocess_text(text)
    assert "this" not in processed_text
    assert "is" not in processed_text
    assert "a" not in processed_text
    assert "test" in processed_text


def test_preprocessor_lemmatization(preprocessor):
    text = "Running"
    processed_text = preprocessor.preprocess_text(text)
    assert processed_text == "run"
