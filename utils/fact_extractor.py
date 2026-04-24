"""
Fact Extractor: LLM-based extraction of user facts with conflict detection.

Uses OpenAI to parse user messages and extract structured facts.
Handles conflicts when new facts contradict existing profile data.
"""
from __future__ import annotations

import json
import re
from typing import Any

from langchain_openai import ChatOpenAI

from agent.prompt import FACT_EXTRACTION_PROMPT
import config


def extract_facts_from_message(
    user_message: str,
    current_profile: dict[str, Any],
    recent_context: str,
    llm: ChatOpenAI | None = None,
) -> dict[str, Any]:
    """
    Extract facts from user message using LLM.
    
    Returns dict with keys:
        - facts: dict of extracted key-value facts
        - episode_summary: str summary if worth saving
        - episode_outcome: str outcome/lesson
        - has_conflict: bool
        - conflict_details: str
    """
    if llm is None:
        llm = ChatOpenAI(
            model=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY,
            temperature=0,
        )

    # Format current profile for prompt
    profile_str = json.dumps(current_profile, ensure_ascii=False, indent=2) if current_profile else "{}"

    prompt = FACT_EXTRACTION_PROMPT.format(
        user_message=user_message,
        current_profile=profile_str,
        recent_context=recent_context or "Không có context trước đó.",
    )

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        # Try to parse JSON from response
        result = _parse_json_response(content)

        # Validate structure
        if "facts" not in result:
            result["facts"] = {}
        if "episode_summary" not in result:
            result["episode_summary"] = ""
        if "episode_outcome" not in result:
            result["episode_outcome"] = ""
        if "has_conflict" not in result:
            result["has_conflict"] = False
        if "conflict_details" not in result:
            result["conflict_details"] = ""

        return result

    except Exception as e:
        # Fallback: return empty extraction on error
        print(f"[FactExtractor] Error: {e}")
        return {
            "facts": {},
            "episode_summary": "",
            "episode_outcome": "",
            "has_conflict": False,
            "conflict_details": "",
        }


def _parse_json_response(content: str) -> dict:
    """Parse JSON from LLM response, handling common formatting issues."""
    # Try direct parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try to find JSON block in markdown code fence
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find JSON object in text
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback
    return {"facts": {}, "episode_summary": "", "episode_outcome": "", "has_conflict": False, "conflict_details": ""}
