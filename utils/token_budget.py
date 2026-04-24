"""
Token Budget: Token counting and trimming utilities.

Uses tiktoken for accurate token counting.
Implements trim logic to keep memory context within budget.
"""
from __future__ import annotations

import tiktoken


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count tokens in text using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def trim_text_to_budget(text: str, max_tokens: int, model: str = "gpt-4o-mini") -> str:
    """
    Trim text to fit within token budget.
    Keeps the beginning of the text (most important context).
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text

    trimmed_tokens = tokens[:max_tokens]
    return encoding.decode(trimmed_tokens) + "\n... [đã cắt bớt do vượt quá budget token]"


def allocate_token_budget(
    total_budget: int,
    profile_text: str,
    episodes_text: str,
    semantic_text: str,
    conversation_text: str,
    model: str = "gpt-4o-mini",
) -> dict[str, str]:
    """
    Phân bổ token budget cho 4 loại memory.
    
    Ưu tiên: profile > semantic > episodic > conversation
    Mỗi loại được tối đa 30% budget, phần dư chia cho conversation.
    
    Returns dict với 4 keys đã được trim.
    """
    # Count tokens for each section
    counts = {
        "profile": count_tokens(profile_text, model),
        "episodes": count_tokens(episodes_text, model),
        "semantic": count_tokens(semantic_text, model),
        "conversation": count_tokens(conversation_text, model),
    }

    total_needed = sum(counts.values())

    # If everything fits comfortably, no trimming needed
    if total_needed <= total_budget:
        return {
            "profile": profile_text,
            "episodes": episodes_text,
            "semantic": semantic_text,
            "conversation": conversation_text,
        }

    # Allocate budget with priorities
    # Profile gets up to 20%, semantic up to 25%, episodic up to 25%, conversation gets rest
    allocations = {
        "profile": min(counts["profile"], int(total_budget * 0.20)),
        "semantic": min(counts["semantic"], int(total_budget * 0.25)),
        "episodes": min(counts["episodes"], int(total_budget * 0.25)),
    }
    allocations["conversation"] = total_budget - sum(allocations.values())

    return {
        "profile": trim_text_to_budget(profile_text, allocations["profile"], model),
        "episodes": trim_text_to_budget(episodes_text, allocations["episodes"], model),
        "semantic": trim_text_to_budget(semantic_text, allocations["semantic"], model),
        "conversation": trim_text_to_budget(conversation_text, allocations["conversation"], model),
    }
