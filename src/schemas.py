"""
ATHENA's canonical structured state schema.

Every LLM extraction must conform to these models before
the data is allowed into the rest of the system.
"""

from pydantic import BaseModel, Field


class EmotionalState(BaseModel):
    """Normalized behavioral/emotional state representation."""

    stress: float = Field(ge=0.0, le=1.0)
    anxiety: float = Field(ge=0.0, le=1.0)
    motivation: float = Field(ge=0.0, le=1.0)
    fatigue: float = Field(ge=0.0, le=1.0)
    social_connection: float = Field(ge=0.0, le=1.0)


class ATHENAState(BaseModel):
    """
    Complete structured representation extracted from one
    journal/conversation entry.
    """

    emotional_state: EmotionalState

    topics: list[str] = Field(default_factory=list)
    linguistic_signals: list[str] = Field(default_factory=list)
    context: list[str] = Field(default_factory=list)

    confidence: float = Field(ge=0.0, le=1.0)
