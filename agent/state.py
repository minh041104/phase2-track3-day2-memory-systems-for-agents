"""
MemoryState: LangGraph state definition for Multi-Memory Agent.

Defines the TypedDict that flows through all graph nodes,
carrying messages + memory context from all 4 backends.
"""
from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class MemoryState(TypedDict):
    """
    State schema cho LangGraph Multi-Memory Agent.
    
    Attributes:
        messages: Conversation messages (auto-appended via add_messages reducer)
        current_input: User's latest input text
        user_profile: Dict of user facts from long-term profile memory
        episodes: List of relevant episodic memories
        semantic_hits: List of semantic search results
        memory_context: Formatted prompt section with all memory injected
        memory_budget: Max tokens allowed for memory context
        should_save: Whether to save/update memory after this turn
        extracted_facts: Facts extracted from user's message for profile update
        episode_summary: Summary of current episode to save
    """
    messages: Annotated[list, add_messages]
    current_input: str
    user_profile: dict[str, Any]
    episodes: list[dict]
    semantic_hits: list[str]
    memory_context: str
    memory_budget: int
    should_save: bool
    extracted_facts: dict[str, Any]
    episode_summary: str
