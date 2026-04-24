"""
Configuration & constants for Multi-Memory Agent.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── OpenAI ──────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"  # cost-effective model for lab

# ── Token Budget ────────────────────────────────────────
MAX_TOKEN_BUDGET = 4000       # max tokens for memory context in prompt
TRIM_TARGET_TOKENS = 3000     # target after trimming

# ── Short-term Memory ──────────────────────────────────
SLIDING_WINDOW_SIZE = 10      # keep last N message pairs

# ── Data Paths ──────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PROFILE_PATH = os.path.join(DATA_DIR, "user_profile.json")
EPISODES_PATH = os.path.join(DATA_DIR, "episodes.json")
CHROMA_DB_PATH = os.path.join(DATA_DIR, "chroma_db")

# ── Semantic Memory ────────────────────────────────────
SEMANTIC_COLLECTION_NAME = "knowledge_base"
SEMANTIC_TOP_K = 3            # number of results to retrieve

# ── Episodic Memory ───────────────────────────────────
MAX_EPISODES_IN_PROMPT = 5    # max episodes to include in prompt

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
