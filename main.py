"""
Main: Interactive chat loop with Multi-Memory Agent.

Run: python main.py
Commands:
  /profile  — Xem user profile hiện tại
  /episodes — Xem episodic memories
  /memory   — Xem trạng thái toàn bộ memory
  /clear    — Xóa toàn bộ memory
  /quit     — Thoát
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from agent.graph import create_agent, run_agent_turn
import config


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║         🧠 Multi-Memory Agent with LangGraph 🧠         ║
║                                                          ║
║  Memory Stack:                                           ║
║  📝 Short-term  — Sliding window conversation buffer     ║
║  👤 Long-term   — User profile (JSON KV store)           ║
║  📖 Episodic    — Task outcomes & lessons (JSON log)     ║
║  🔍 Semantic    — Knowledge base (ChromaDB vectors)      ║
║                                                          ║
║  Commands: /profile /episodes /memory /clear /quit       ║
╚══════════════════════════════════════════════════════════╝
""")


def handle_command(command: str, memories: dict) -> bool:
    """Handle slash commands. Returns True if command was handled."""
    cmd = command.strip().lower()

    if cmd == "/quit" or cmd == "/exit":
        print("\n👋 Tạm biệt! Memory đã được lưu.")
        return True

    if cmd == "/profile":
        profile = memories["long_term"].get_profile()
        print("\n👤 User Profile:")
        if profile:
            for k, v in profile.items():
                print(f"  • {k}: {v}")
        else:
            print("  (trống)")
        
        # Show change log
        changes = memories["long_term"].get_change_log()
        if changes:
            print(f"\n📋 Change Log ({len(changes)} entries):")
            for c in changes[-5:]:  # last 5
                print(f"  [{c.get('action')}] {c.get('key')}: "
                      f"'{c.get('old_value')}' → '{c.get('new_value', 'deleted')}'")
        print()
        return False

    if cmd == "/episodes":
        episodes = memories["episodic"].get_all_episodes()
        print(f"\n📖 Episodic Memory ({len(episodes)} episodes):")
        if episodes:
            for ep in episodes[-10:]:
                print(f"  [{ep.get('category', '?')}] {ep['summary']}")
                print(f"     → {ep['outcome']}")
        else:
            print("  (trống)")
        print()
        return False

    if cmd == "/memory":
        print("\n🧠 Memory Status:")
        print(f"  📝 Short-term: {memories['short_term'].size} messages "
              f"(window={memories['short_term'].window_size})")
        print(f"  👤 Long-term:  {len(memories['long_term'].get_profile())} facts")
        print(f"  📖 Episodic:   {memories['episodic'].count} episodes")
        print(f"  🔍 Semantic:   {memories['semantic'].count} documents")
        print()
        return False

    if cmd == "/clear":
        memories["short_term"].clear()
        memories["long_term"].clear()
        memories["episodic"].clear()
        print("🗑️  Đã xóa Short-term, Long-term, và Episodic memory.")
        print("   (Semantic knowledge base giữ nguyên)")
        print()
        return False

    return False


def main():
    print_banner()

    # Check API key
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your-openai-api-key-here":
        print("❌ Chưa set OPENAI_API_KEY!")
        print("   Tạo file .env với nội dung: OPENAI_API_KEY=sk-...")
        print("   Hoặc copy .env.example → .env và điền API key.")
        sys.exit(1)

    # Create agent
    print("⏳ Đang khởi tạo agent...")
    graph, memories, graph_config = create_agent(use_memory=True, thread_id="interactive")
    print(f"✅ Agent sẵn sàng! ({config.MODEL_NAME})")
    print(f"   Memory: {memories['semantic'].count} documents trong knowledge base\n")

    # Chat loop
    turn = 0
    while True:
        try:
            user_input = input("🧑 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Tạm biệt!")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith("/"):
            should_quit = handle_command(user_input, memories)
            if should_quit:
                break
            continue

        # Run agent
        turn += 1
        print(f"\n⏳ Đang xử lý (turn {turn})...")

        try:
            response = run_agent_turn(graph, user_input, graph_config)
            print(f"\n🤖 Agent: {response}\n")

            # Show memory update status
            profile = memories["long_term"].get_profile()
            if profile:
                facts_str = ", ".join(f"{k}={v}" for k, v in list(profile.items())[:3])
                print(f"  💾 Profile: {facts_str}{'...' if len(profile) > 3 else ''}")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main()
