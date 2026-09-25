"""
Layer 2 (semantic half): turns entry text into a vector so future
layers (semantic memory search, clustering triggers, etc.) have
something to work with beyond the LLM's structured tags.

Local model, no API key needed — keeps this fast/cheap since it runs
on every single entry.
"""
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        # Imported lazily: this import + model load is the slow part
        # (~1-2s first call), don't pay that cost unless embeddings
        # are actually requested.
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed(text: str) -> np.ndarray:
    """Returns a 384-dim float32 vector for the given text."""
    model = _get_model()
    vec = model.encode(text, convert_to_numpy=True)
    return vec.astype(np.float32)
