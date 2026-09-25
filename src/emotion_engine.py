"""
Layer 1: Multimodal NLP (text-only for now).

Uses Gemini to extract a structured behavioral/emotional state from
a journal-style entry. Pydantic validates the result before it enters
the rest of the ATHENA pipeline.
"""

from google import genai

from src.config import GEMINI_API_KEY, ATHENA_MODEL, STATE_DIMENSIONS
from src.schemas import ATHENAState


_client = None


def _get_client():
    """Create the Gemini client lazily."""
    global _client

    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. "
                "Add your key to the .env file."
            )

        _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client


SYSTEM_PROMPT = f"""
You are the extraction layer of ATHENA, a longitudinal behavioral
and emotional state-tracking research system.

You are NOT a therapist and you do NOT provide advice or clinical
diagnoses.

Given one journal-style text entry, extract an evidence-grounded
snapshot of the writer's linguistic and behavioral state.

Track these dimensions:

{", ".join(STATE_DIMENSIONS)}

Each dimension must be scored from 0.0 to 1.0.

Interpretation:

0.0 = very low signal
0.5 = neutral or unclear
1.0 = very strong signal

Important:

- Score ONLY what the text supports.
- Do not assume information that is not present.
- 0.5 means neutral/unclear, NOT the average human.
- A very short entry should have lower confidence.
- Do not infer clinical diagnoses.
- Do not provide advice.
- Topics should be short descriptive phrases.
- Linguistic signals should describe observable characteristics
  of the text.
- Context should contain contextual factors explicitly mentioned
  or strongly implied by the entry.
- Confidence should reflect how much usable signal is present.
"""


def analyze(text: str) -> dict:
    """
    Analyze one journal entry and return a validated ATHENA state.

    Gemini produces JSON constrained by the ATHENAState schema,
    and Pydantic validates the final result.
    """

    if not text or not text.strip():
        raise ValueError("Journal entry cannot be empty.")

    client = _get_client()

    interaction = client.interactions.create(
    model=ATHENA_MODEL,
    system_instruction=SYSTEM_PROMPT,
    input=text,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": ATHENAState.model_json_schema(),
    },
)

    state = ATHENAState.model_validate_json(
        interaction.output_text
    )

    result = state.model_dump()

    # Preserve the original journal entry for downstream storage.
    result["text"] = text

    return result