"""
Graph Nodes: Functions that operate on MemoryState within the LangGraph.

Nodes:
1. retrieve_memory — Router: gom memory từ 4 backends → inject vào state
2. generate_response — Gọi LLM với prompt đã inject memory
3. save_memory — Extract facts, update profile + episodic memory
"""
from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from agent.state import MemoryState
from agent.prompt import SYSTEM_PROMPT_TEMPLATE
from memory.short_term import ShortTermMemory
from memory.long_term_profile import LongTermProfileMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from utils.token_budget import allocate_token_budget, count_tokens
from utils.fact_extractor import extract_facts_from_message
import config


# ── Global memory instances (injected at graph creation) ─────
_short_term: ShortTermMemory | None = None
_long_term: LongTermProfileMemory | None = None
_episodic: EpisodicMemory | None = None
_semantic: SemanticMemory | None = None
_llm: ChatOpenAI | None = None


def init_memories(
    short_term: ShortTermMemory,
    long_term: LongTermProfileMemory,
    episodic: EpisodicMemory,
    semantic: SemanticMemory,
    llm: ChatOpenAI,
) -> None:
    """Initialize global memory references. Called once at graph creation."""
    global _short_term, _long_term, _episodic, _semantic, _llm
    _short_term = short_term
    _long_term = long_term
    _episodic = episodic
    _semantic = semantic
    _llm = llm


# ═══════════════════════════════════════════════════════════
# Node 1: RETRIEVE MEMORY
# ═══════════════════════════════════════════════════════════

def retrieve_memory(state: MemoryState) -> dict[str, Any]:
    """
    Router node: gom memory từ 4 backends, format, và inject vào state.
    
    Flow:
    1. Lấy user_profile từ long-term
    2. Lấy recent episodes từ episodic
    3. Search semantic memory bằng current_input
    4. Lấy recent conversation từ short-term
    5. Apply token budget → trim nếu cần
    6. Build memory_context string cho prompt
    """
    user_input = state.get("current_input", "")

    # 1. Long-term Profile
    profile = _long_term.get_profile() if _long_term else {}
    profile_text = _long_term.format_for_prompt() if _long_term else ""

    # 2. Episodic Memory
    episodes_raw = _episodic.get_recent_episodes(config.MAX_EPISODES_IN_PROMPT) if _episodic else []
    episodes_text = _episodic.format_for_prompt(config.MAX_EPISODES_IN_PROMPT) if _episodic else ""

    # 3. Semantic Memory (search bằng user input)
    semantic_hits_raw = []
    semantic_text = ""
    if _semantic and user_input:
        semantic_text = _semantic.format_for_prompt(user_input, config.SEMANTIC_TOP_K)
        hits = _semantic.search(user_input, config.SEMANTIC_TOP_K)
        semantic_hits_raw = [h["document"] for h in hits]

    # 4. Short-term Conversation
    conversation_text = _short_term.format_for_prompt() if _short_term else ""

    # 5. Apply Token Budget
    budget = state.get("memory_budget", config.MAX_TOKEN_BUDGET)
    trimmed = allocate_token_budget(
        total_budget=budget,
        profile_text=profile_text,
        episodes_text=episodes_text,
        semantic_text=semantic_text,
        conversation_text=conversation_text,
    )

    # 6. Build memory context for prompt
    memory_context = SYSTEM_PROMPT_TEMPLATE.format(
        user_profile=trimmed["profile"],
        episodes=trimmed["episodes"],
        semantic_hits=trimmed["semantic"],
        recent_conversation=trimmed["conversation"],
    )

    return {
        "user_profile": profile,
        "episodes": episodes_raw,
        "semantic_hits": semantic_hits_raw,
        "memory_context": memory_context,
    }


# ═══════════════════════════════════════════════════════════
# Node 2: GENERATE RESPONSE
# ═══════════════════════════════════════════════════════════

def generate_response(state: MemoryState) -> dict[str, Any]:
    """
    Gọi LLM với prompt đã inject memory context.
    
    Prompt structure:
    - System: memory_context (chứa 4 sections memory)
    - Messages: conversation history (managed by LangGraph add_messages)
    """
    memory_context = state.get("memory_context", "")
    user_input = state.get("current_input", "")

    # Build messages for LLM
    messages = [
        SystemMessage(content=memory_context),
        HumanMessage(content=user_input),
    ]

    # Call LLM
    response = _llm.invoke(messages)

    # Update short-term memory
    if _short_term:
        _short_term.add_message("user", user_input)
        _short_term.add_message("assistant", response.content)

    return {
        "messages": [HumanMessage(content=user_input), response],
    }


# ═══════════════════════════════════════════════════════════
# Node 3: SAVE MEMORY
# ═══════════════════════════════════════════════════════════

def save_memory(state: MemoryState) -> dict[str, Any]:
    """
    Extract facts từ conversation và update memory backends.
    
    1. Dùng LLM extract facts từ user message
    2. Update long-term profile (with conflict handling)
    3. Save episodic memory nếu có episode đáng ghi
    """
    user_input = state.get("current_input", "")
    current_profile = _long_term.get_profile() if _long_term else {}
    recent_context = _short_term.format_for_prompt() if _short_term else ""

    # Extract facts using LLM
    extraction = extract_facts_from_message(
        user_message=user_input,
        current_profile=current_profile,
        recent_context=recent_context,
        llm=_llm,
    )

    extracted_facts = extraction.get("facts", {})
    episode_summary = extraction.get("episode_summary", "")
    episode_outcome = extraction.get("episode_outcome", "")

    # Update long-term profile
    update_results = []
    if extracted_facts and _long_term:
        update_results = _long_term.update_facts(extracted_facts)
        for result in update_results:
            if result.get("action") == "updated (conflict resolved)":
                print(f"  ⚠ Conflict resolved: {result['key']}: "
                      f"'{result['old_value']}' → '{result['new_value']}'")

    # Save episodic memory
    if episode_summary and _episodic:
        _episodic.add_episode(
            summary=episode_summary,
            outcome=episode_outcome or "Không có kết quả cụ thể",
            category=extraction.get("category", "conversation"),
        )

    return {
        "extracted_facts": extracted_facts,
        "episode_summary": episode_summary,
        "should_save": bool(extracted_facts or episode_summary),
    }


# ═══════════════════════════════════════════════════════════
# Conditional Edge: SHOULD SAVE?
# ═══════════════════════════════════════════════════════════

def should_save_memory(state: MemoryState) -> str:
    """
    Conditional edge: decide whether to run save_memory node.
    Always save to allow LLM to extract any implicit facts.
    Returns next node name.
    """
    return "save_memory"
