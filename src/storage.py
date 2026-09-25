"""
Layer 3: Semantic memory. SQLite for now — one serious database beats
three half-configured ones on day 1. Swap for Postgres+pgvector later
by reimplementing this module; callers shouldn't need to change.
"""
import json
import sqlite3
from datetime import datetime, timedelta, timezone

import numpy as np

from src.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL DEFAULT 'default_user',
    text TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    emotional_state TEXT NOT NULL,   -- JSON dict of dimension -> score
    topics TEXT NOT NULL,            -- JSON list
    linguistic_signals TEXT NOT NULL,-- JSON list
    context TEXT NOT NULL,           -- JSON list
    confidence REAL NOT NULL,
    embedding BLOB                   -- float32 numpy bytes, nullable
);
"""


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    return conn


def save_entry(
    analysis: dict,
    embedding: np.ndarray | None = None,
    user_id: str = "default_user",
    days_ago: int = 0,
) -> int:
    """Persists one analyzed entry. Returns its row id."""
    timestamp = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    conn = _connect()
    try:
        cur = conn.execute(
            """INSERT INTO entries
               (user_id, text, timestamp, emotional_state, topics,
                linguistic_signals, context, confidence, embedding)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                analysis["text"],
                timestamp,
                json.dumps(analysis["emotional_state"]),
                json.dumps(analysis.get("topics", [])),
                json.dumps(analysis.get("linguistic_signals", [])),
                json.dumps(analysis.get("context", [])),
                float(analysis.get("confidence", 0.5)),
                embedding.tobytes() if embedding is not None else None,
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_entries(user_id: str = "default_user") -> list[dict]:
    """Returns all entries for a user, oldest first."""
    conn = _connect()
    try:
        rows = conn.execute(
            """SELECT id, text, timestamp, emotional_state, topics,
                      linguistic_signals, context, confidence
               FROM entries WHERE user_id = ? ORDER BY timestamp ASC""",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    entries = []
    for r in rows:
        entries.append(
            {
                "id": r[0],
                "text": r[1],
                "timestamp": r[2],
                "emotional_state": json.loads(r[3]),
                "topics": json.loads(r[4]),
                "linguistic_signals": json.loads(r[5]),
                "context": json.loads(r[6]),
                "confidence": r[7],
            }
        )
    return entries
