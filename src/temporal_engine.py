"""
Layer 4: Temporal reasoning. Deliberately simple for v0 — mean/threshold
based, not a real change-point algorithm yet (e.g. PELT, Bayesian online
change-point detection). That upgrade is a Day 3 task once we can see
real data and know these numbers are trustworthy.
"""
from src.config import STATE_DIMENSIONS


def personal_baseline(entries: list[dict], exclude_last_n: int = 3) -> dict:
    """
    The user's own historical average for each state dimension,
    excluding the most recent N entries (those form the "current window"
    being compared against the baseline, not part of it).
    """
    history = entries[:-exclude_last_n] if len(entries) > exclude_last_n else []
    if not history:
        return {dim: 0.5 for dim in STATE_DIMENSIONS}

    baseline = {}
    for dim in STATE_DIMENSIONS:
        values = [e["emotional_state"].get(dim, 0.5) for e in history]
        baseline[dim] = sum(values) / len(values)
    return baseline


def current_window(entries: list[dict], window_n: int = 3) -> dict:
    """Average state over the most recent N entries."""
    recent = entries[-window_n:] if entries else []
    if not recent:
        return {dim: 0.5 for dim in STATE_DIMENSIONS}

    window = {}
    for dim in STATE_DIMENSIONS:
        values = [e["emotional_state"].get(dim, 0.5) for e in recent]
        window[dim] = sum(values) / len(values)
    return window


def compare_to_baseline(entries: list[dict], window_n: int = 3) -> dict:
    """
    Returns, per dimension: baseline, current, delta, and whether that
    delta crosses a naive "meaningful change" threshold (0.2 absolute).
    This threshold is a placeholder — tune it once you have real data.
    """
    baseline = personal_baseline(entries, exclude_last_n=window_n)
    current = current_window(entries, window_n=window_n)

    THRESHOLD = 0.2
    result = {}
    for dim in STATE_DIMENSIONS:
        delta = current[dim] - baseline[dim]
        result[dim] = {
            "baseline": round(baseline[dim], 3),
            "current": round(current[dim], 3),
            "delta": round(delta, 3),
            "flagged": abs(delta) >= THRESHOLD,
        }
    return result


def trajectory(entries: list[dict], dimension: str) -> list[tuple[str, float]]:
    """Returns (timestamp, score) pairs for one dimension, in order."""
    if dimension not in STATE_DIMENSIONS:
        raise ValueError(f"Unknown dimension '{dimension}'. Choose from {STATE_DIMENSIONS}")
    return [(e["timestamp"], e["emotional_state"].get(dimension, 0.5)) for e in entries]
