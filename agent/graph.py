"""
LangGraph StateGraph builder for Multi-Memory Agent.

Graph flow:
  START → retrieve_memory → generate_response → save_memory → END

This module builds and compiles the graph, and provides a convenience
function to create a fully configured agent instance.
"""
from __future__ import annotations

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI

from agent.state import MemoryState
from agent.nodes import (
    retrieve_memory,
    generate_response,
    save_memory,
    should_save_memory,
    init_memories,
)
from memory.short_term import ShortTermMemory
from memory.long_term_profile import LongTermProfileMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
import config


def build_graph() -> StateGraph:
    """
    Build the LangGraph StateGraph with 3 nodes:
    
    1. retrieve_memory — Router gom memory từ 4 backends
    2. generate_response — Gọi LLM với injected memory
    3. save_memory — Extract & persist facts/episodes
    
    Flow: START → retrieve → generate → (conditional) save → END
    """
    builder = StateGraph(MemoryState)

    # Add nodes
    builder.add_node("retrieve_memory", retrieve_memory)
    builder.add_node("generate_response", generate_response)
    builder.add_node("save_memory", save_memory)

    # Add edges
    builder.add_edge(START, "retrieve_memory")
    builder.add_edge("retrieve_memory", "generate_response")

    # Conditional edge: after generate, decide whether to save
    builder.add_conditional_edges(
        "generate_response",
        should_save_memory,
        {
            "save_memory": "save_memory",
            "end": END,
        },
    )
    builder.add_edge("save_memory", END)

    return builder


def create_agent(
    use_memory: bool = True,
    thread_id: str = "default",
) -> tuple:
    """
    Create a fully configured Multi-Memory Agent.
    
    Args:
        use_memory: If False, creates agent without memory (for benchmark comparison)
        thread_id: Thread ID for checkpointer
        
    Returns:
        Tuple of (compiled_graph, memories_dict, config_dict)
    """
    # Initialize LLM
    llm = ChatOpenAI(
        model=config.MODEL_NAME,
        api_key=config.OPENAI_API_KEY,
        temperature=0.7,
    )

    # Initialize memory backends
    short_term = ShortTermMemory(window_size=config.SLIDING_WINDOW_SIZE)
    long_term = LongTermProfileMemory(filepath=config.PROFILE_PATH)
    episodic = EpisodicMemory(filepath=config.EPISODES_PATH)
    semantic = SemanticMemory(
        persist_directory=config.CHROMA_DB_PATH,
        collection_name=config.SEMANTIC_COLLECTION_NAME,
    )

    if not use_memory:
        # For no-memory mode: use empty/dummy memories that don't persist
        short_term = ShortTermMemory(window_size=0)
        long_term = LongTermProfileMemory(filepath=config.PROFILE_PATH + ".nomem")
        long_term.clear()
        episodic = EpisodicMemory(filepath=config.EPISODES_PATH + ".nomem")
        episodic.clear()

    # Initialize global memory references in nodes module
    init_memories(short_term, long_term, episodic, semantic, llm)

    # Build and compile graph
    builder = build_graph()
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)

    memories = {
        "short_term": short_term,
        "long_term": long_term,
        "episodic": episodic,
        "semantic": semantic,
    }

    graph_config = {"configurable": {"thread_id": thread_id}}

    return graph, memories, graph_config


def run_agent_turn(
    graph,
    user_input: str,
    graph_config: dict,
    memory_budget: int = config.MAX_TOKEN_BUDGET,
) -> str:
    """
    Run a single turn of the agent.
    
    Args:
        graph: Compiled LangGraph
        user_input: User's message
        graph_config: Config with thread_id
        memory_budget: Token budget for memory context
        
    Returns:
        Agent's response text
    """
    state_input = {
        "current_input": user_input,
        "memory_budget": memory_budget,
        "messages": [],
        "user_profile": {},
        "episodes": [],
        "semantic_hits": [],
        "memory_context": "",
        "should_save": False,
        "extracted_facts": {},
        "episode_summary": "",
    }

    result = graph.invoke(state_input, config=graph_config)

    # Extract assistant's response from messages
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and (
            getattr(msg, "type", None) == "ai" or
            isinstance(msg, type) and msg.__class__.__name__ == "AIMessage"
        ):
            return msg.content

    # Fallback: try last message
    if messages:
        last = messages[-1]
        if hasattr(last, "content"):
            return last.content

    return "Xin lỗi, tôi không thể tạo phản hồi."
