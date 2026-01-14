import pytest

from PyBot.bot.core.models.svc_model import SVCModel


@pytest.fixture
def svc_model():
    return SVCModel()


def test_svc_model_initialization(svc_model):
    assert svc_model is not None
    assert svc_model.pipeline is not None


def test_svc_model_train(svc_model):
    intents = [
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
    ]
    trained_model = svc_model.train(intents)
    assert trained_model is not None


def test_svc_model_predict(svc_model):
    intents = [
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
    ]
    trained_model = svc_model.train(intents)
    prediction = svc_model.predict(["Hello"])
    assert prediction is not None
    assert isinstance(prediction, list)
    assert len(prediction) > 0
