"""
ATHENA demo dataset.

Creates a small deterministic longitudinal dataset for presentations.
This is DEMO DATA only; it does not bypass the production extraction
pipeline.
"""

import numpy as np

from src import storage


DEMO_ENTRIES = [
    {
        "text": "I had a fairly normal day. I finished most of my planned work and had some time to relax in the evening.",
        "emotional_state": {
            "stress": 0.25,
            "anxiety": 0.25,
            "motivation": 0.65,
            "fatigue": 0.35,
            "social_connection": 0.55,
        },
        "topics": ["daily routine", "work productivity"],
        "linguistic_signals": ["calm tone", "goal completion"],
        "context": ["routine day"],
        "confidence": 0.65,
        "days_ago": 4,
    },
    {
        "text": "I have more work than usual today. I am getting a little worried about keeping up, but I think I can manage it.",
        "emotional_state": {
            "stress": 0.40,
            "anxiety": 0.40,
            "motivation": 0.70,
            "fatigue": 0.45,
            "social_connection": 0.50,
        },
        "topics": ["increased workload"],
        "linguistic_signals": ["mild worry", "goal orientation"],
        "context": ["increased workload"],
        "confidence": 0.70,
        "days_ago": 3,
    },
    {
        "text": "Three deadlines are getting close and I keep thinking about whether I will finish everything. I am tired and finding it harder to focus.",
        "emotional_state": {
            "stress": 0.70,
            "anxiety": 0.65,
            "motivation": 0.65,
            "fatigue": 0.70,
            "social_connection": 0.45,
        },
        "topics": ["deadlines", "workload", "focus"],
        "linguistic_signals": ["anticipatory worry", "fatigue"],
        "context": ["upcoming deadlines"],
        "confidence": 0.78,
        "days_ago": 2,
    },
    {
        "text": "The deadlines are really stressing me out now. I barely took a break today and I feel exhausted, although I still want to finish the work.",
        "emotional_state": {
            "stress": 0.85,
            "anxiety": 0.80,
            "motivation": 0.70,
            "fatigue": 0.90,
            "social_connection": 0.40,
        },
        "topics": ["deadline pressure", "exhaustion"],
        "linguistic_signals": ["high stress", "strong fatigue", "goal persistence"],
        "context": ["deadline pressure", "limited breaks"],
        "confidence": 0.88,
        "days_ago": 1,
    },
    {
        "text": "I finally submitted most of the work. I feel much less stressed today and have more energy. I still have some things left, but I feel in control again.",
        "emotional_state": {
            "stress": 0.35,
            "anxiety": 0.30,
            "motivation": 0.75,
            "fatigue": 0.40,
            "social_connection": 0.55,
        },
        "topics": ["task completion", "recovery"],
        "linguistic_signals": ["reduced stress", "increased agency"],
        "context": ["work submitted"],
        "confidence": 0.82,
        "days_ago": 0,
    },
]


def main():
    print("Creating ATHENA demo dataset...")

    for entry in DEMO_ENTRIES:
        analysis = {
            key: entry[key]
            for key in (
                "text",
                "emotional_state",
                "topics",
                "linguistic_signals",
                "context",
                "confidence",
            )
        }

        # Demo entries do not need semantic vectors.
        storage.save_entry(
            analysis,
            embedding=np.zeros(384, dtype=np.float32),
            days_ago=entry["days_ago"],
        )

    print(f"Added {len(DEMO_ENTRIES)} demo entries.")


if __name__ == "__main__":
    main()
