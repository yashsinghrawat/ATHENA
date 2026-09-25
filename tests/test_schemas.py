import pytest
from pydantic import ValidationError

from src.schemas import ATHENAState


def test_valid_state():
    state = ATHENAState(
        emotional_state={
            "stress": 0.8,
            "anxiety": 0.6,
            "motivation": 0.4,
            "fatigue": 0.7,
            "social_connection": 0.5,
        },
        topics=["deadlines", "work"],
        linguistic_signals=["future-oriented worry"],
        context=["deadlines"],
        confidence=0.9,
    )

    assert state.emotional_state.stress == 0.8
    assert state.confidence == 0.9


def test_invalid_score_rejected():
    with pytest.raises(ValidationError):
        ATHENAState(
            emotional_state={
                "stress": 1.5,
                "anxiety": 0.5,
                "motivation": 0.5,
                "fatigue": 0.5,
                "social_connection": 0.5,
            },
            confidence=0.8,
        )


def test_invalid_confidence_rejected():
    with pytest.raises(ValidationError):
        ATHENAState(
            emotional_state={
                "stress": 0.5,
                "anxiety": 0.5,
                "motivation": 0.5,
                "fatigue": 0.5,
                "social_connection": 0.5,
            },
            confidence=1.5,
        )