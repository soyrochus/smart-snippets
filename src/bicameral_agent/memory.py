"""Persistent state management for bicameral agent."""
from __future__ import annotations

import json
import os
from typing import Dict


MEMORY_FILE = os.path.join(os.path.dirname(__file__), "agent_state.json")
INIT_MEMORY = False  # If True, create the memory file if missing

def get_memory() -> dict:
    """Return the current agent state from ``MEMORY_FILE``."""
    if not os.path.exists(MEMORY_FILE):
        if INIT_MEMORY:
            state = {"step": 0, "history": [], "complete": False}
            with open(MEMORY_FILE, "w", encoding="utf-8") as fh:
                json.dump(state, fh)
            return state
        return {"step": 0, "history": [], "complete": False}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError:
        return {"step": 0, "history": [], "complete": False}


def update_memory(state: dict) -> None:
    """Persist ``state`` to ``MEMORY_FILE``."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh)

