"""Central config, loaded from .env."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ATHENA_MODEL = os.getenv("ATHENA_MODEL", "gemini-3.5-flash-lite")
DB_PATH = ROOT / os.getenv("ATHENA_DB_PATH", "data/athena.db")

# The state dimensions ATHENA tracks. Keep this list stable — the
# temporal engine assumes every extraction has exactly these keys.
STATE_DIMENSIONS = [
    "stress",
    "anxiety",
    "motivation",
    "fatigue",
    "social_connection",
]
