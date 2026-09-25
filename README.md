# ATHENA
### Affective Thought & Human Experience Neural Analysis

A longitudinal AI system that builds an evolving representation of a person's
behavioral/emotional state from text over time, compares it to *their own*
personal baseline, and explains what changed and why — instead of just
reacting to single messages.

This is **not** a chatbot and **not** a diagnostic tool. It never outputs
clinical labels ("you are depressed"). It outputs observed linguistic/semantic
drift from a personal baseline, with evidence and a confidence score.

## What's actually built right now (Phase 1 — AI Core)

```
TEXT ENTRY
    │
    ▼
LLM STRUCTURED EXTRACTION   (src/emotion_engine.py)
    │  → stress / motivation / fatigue / anxiety / social scores
    │  → topics, linguistic signals, confidence
    ▼
EMBEDDING                   (src/embedding_engine.py)
    │  → sentence-transformers vector for the entry
    ▼
SEMANTIC MEMORY (SQLite)    (src/storage.py)
    │  → every entry + its state vector + embedding, timestamped
    ▼
TEMPORAL ENGINE             (src/temporal_engine.py)
    │  → personal baseline (rolling mean over your own history)
    │  → current window vs baseline delta
    │  → simple change-point flag when drift exceeds threshold
    ▼
CLI OUTPUT                  (src/main.py)
```

Everything downstream of this (Cognitive State Graph, voice/multimodal,
FastAPI backend, React dashboard, Neo4j) is **intentionally not built yet** —
per the roadmap, get the core loop genuinely working before wrapping product
around it.

## Setup (Fedora / any Linux)

```bash
cd athena
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and paste your ANTHROPIC_API_KEY
```

First run downloads the embedding model (~90MB, one-time, no API key needed
for that part).

## Usage

```bash
# Add a journal-style entry — this runs the full pipeline and stores it
python -m src.main add "I've been struggling to focus lately, barely slept before the exam"

# Add a few more across different (simulated) days to build history
python -m src.main add "Feeling a bit better today, went for a run" --days-ago 2
python -m src.main add "Another all-nighter, I don't think I can keep this up" --days-ago 1

# See your personal baseline vs current window
python -m src.main baseline

# See the raw trajectory of a specific state over time
python -m src.main trajectory stress
```

`--days-ago N` is a dev/demo convenience so you can simulate a history
without waiting real days — remove it once you're logging live entries.

## Why this design (not over-engineered on day 1)

- **One database (SQLite)**, not Postgres+pgvector+Mongo+FAISS. Swap to
  pgvector later — the `storage.py` interface won't need to change much.
- **No graph DB yet.** The Cognitive State Graph (Neo4j) is Week 4 material —
  building it before the state extraction is reliable would be building on
  sand.
- **No frontend yet.** CLI output first so you can actually validate the
  numbers are meaningful before styling them.
- **Single LLM call per entry** for extraction (Claude), not a chain of five
  agents — cheaper, faster, and good enough to prove the concept.

## Roadmap (from here)

| Day | What |
|---|---|
| 1–2 (done by this scaffold) | LLM extraction, embeddings, storage, baseline/trend |
| 3 | Change-point detection refinement, evidence extraction quality pass |
| 4 | Minimal FastAPI wrapper over the same core (2–3 endpoints) |
| 5 | Basic HTML/React dashboard hitting that API (timeline + baseline bars) |
| 6–7 | Polish demo path: seed realistic multi-day data, screenshot/record it |

Multimodal (voice), the graph DB, and auth are explicitly **after** this
week — don't let them creep into the "MVP" scope.

## Research grounding

See `docs/research-notes.md` (add your own notes as you read) — the framing
that current LLMs are inconsistent at interpreting longitudinal
digital-phenotyping data (npj Digital Medicine 2026; BMJ Mental Health 2025)
is your actual research motivation: this project is testing/improving that,
not assuming it's already solved.
