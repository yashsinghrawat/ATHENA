"""
Tests for temporal_engine only — deliberately no API/network calls here,
so this runs in CI without a key. emotion_engine/embedding_engine would
need mocking to be unit-tested the same way; that's a good Day 3 task.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import temporal_engine
from src.config import STATE_DIMENSIONS


def _entry(stress, motivation=0.5, fatigue=0.5, anxiety=0.5, social=0.5, ts="t"):
    return {
        "timestamp": ts,
        "emotional_state": {
            "stress": stress,
            "motivation": motivation,
            "fatigue": fatigue,
            "anxiety": anxiety,
            "social_connection": social,
        },
    }


def test_baseline_excludes_recent_window():
    entries = [_entry(0.3, ts=f"t{i}") for i in range(5)] + [_entry(0.9, ts=f"t{i}") for i in range(5, 8)]
    baseline = temporal_engine.personal_baseline(entries, exclude_last_n=3)
    assert abs(baseline["stress"] - 0.3) < 1e-6, "baseline should only reflect the older, low-stress entries"


def test_current_window_uses_recent_only():
    entries = [_entry(0.3, ts=f"t{i}") for i in range(5)] + [_entry(0.9, ts=f"t{i}") for i in range(5, 8)]
    window = temporal_engine.current_window(entries, window_n=3)
    assert abs(window["stress"] - 0.9) < 1e-6


def test_compare_to_baseline_flags_large_delta():
    entries = [_entry(0.2, ts=f"t{i}") for i in range(5)] + [_entry(0.9, ts=f"t{i}") for i in range(5, 8)]
    comparison = temporal_engine.compare_to_baseline(entries, window_n=3)
    assert comparison["stress"]["flagged"] is True
    assert comparison["motivation"]["flagged"] is False  # unchanged dimension


def test_trajectory_returns_ordered_pairs():
    entries = [_entry(0.1, ts="a"), _entry(0.5, ts="b"), _entry(0.9, ts="c")]
    points = temporal_engine.trajectory(entries, "stress")
    assert points == [("a", 0.1), ("b", 0.5), ("c", 0.9)]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS: {name}")
