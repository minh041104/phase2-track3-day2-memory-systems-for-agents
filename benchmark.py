"""
Benchmark: Run 10 multi-turn conversations comparing no-memory vs with-memory.

Covers all required test groups:
1. Profile recall
2. Conflict update
3. Episodic recall
4. Semantic retrieval
5. Trim/token budget

Output: Console results + BENCHMARK.md
"""
import sys
import os
import json
import time
from datetime import datetime, timezone

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from agent.graph import create_agent, run_agent_turn
from agent.nodes import init_memories
from memory.short_term import ShortTermMemory
from memory.long_term_profile import LongTermProfileMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from seed_knowledge import seed_knowledge_base
from utils.token_budget import count_tokens
import config

from langchain_openai import ChatOpenAI


# ═══════════════════════════════════════════════════════════
# 10 MULTI-TURN CONVERSATION SCENARIOS
# ═══════════════════════════════════════════════════════════

SCENARIOS = [
    # --- Group 1: Profile Recall ---
    {
        "id": 1,
        "name": "Profile Recall — Nhớ tên user sau nhiều turns",
        "group": "profile_recall",
        "turns": [
            "Xin chào, tôi tên là Linh.",
            "Tôi là sinh viên năm 3 ngành CNTT.",
            "Tôi thích lập trình Python.",
            "Hôm nay trời đẹp quá nhỉ?",
            "À mà sở thích của tôi là chơi guitar.",
            "Bạn có nhớ tên tôi không?",
        ],
        "check_turn": 5,  # 0-indexed, last turn
        "expected_keyword": "Linh",
        "description": "Agent cần nhớ tên user 'Linh' sau 6 turns hội thoại",
    },
    {
        "id": 2,
        "name": "Profile Recall — Nhớ nhiều facts cùng lúc",
        "group": "profile_recall",
        "turns": [
            "Tôi tên Minh, 22 tuổi, sống ở Hà Nội.",
            "Tôi làm việc tại FPT Software.",
            "Cho tôi biết những gì bạn biết về tôi?",
        ],
        "check_turn": 2,
        "expected_keyword": "Minh",
        "description": "Agent cần nhớ tên, tuổi, nơi ở, công việc",
    },

    # --- Group 2: Conflict Update ---
    {
        "id": 3,
        "name": "Conflict Update — Sửa dị ứng",
        "group": "conflict_update",
        "turns": [
            "Tôi dị ứng sữa bò.",
            "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.",
            "Tôi dị ứng gì vậy?",
        ],
        "check_turn": 2,
        "expected_keyword": "đậu nành",
        "description": "Agent cần update dị ứng từ 'sữa bò' → 'đậu nành'",
    },
    {
        "id": 4,
        "name": "Conflict Update — Đổi nghề nghiệp",
        "group": "conflict_update",
        "turns": [
            "Tôi là kỹ sư phần mềm.",
            "Thực ra, tôi vừa chuyển sang làm data scientist.",
            "Nghề nghiệp hiện tại của tôi là gì?",
        ],
        "check_turn": 2,
        "expected_keyword": "data scientist",
        "description": "Agent cần update nghề từ 'kỹ sư phần mềm' → 'data scientist'",
    },

    # --- Group 3: Episodic Recall ---
    {
        "id": 5,
        "name": "Episodic Recall — Nhớ bài học debug",
        "group": "episodic_recall",
        "turns": [
            "Hôm qua tôi debug lỗi Docker cả ngày. Cuối cùng phát hiện ra là phải dùng service name thay vì localhost.",
            "Tôi được bài học quan trọng về networking trong Docker.",
            "Nhắc lại giúp tôi bài học về Docker hôm trước?",
        ],
        "check_turn": 2,
        "expected_keyword": "service name",
        "description": "Agent cần recall bài học 'dùng service name thay vì localhost'",
    },
    {
        "id": 6,
        "name": "Episodic Recall — Nhớ task đã hoàn thành",
        "group": "episodic_recall",
        "turns": [
            "Tôi vừa hoàn thành project deploy API lên Railway thành công.",
            "Tôi đã học được cách setup health check endpoint.",
            "Nhắc tôi về project gần đây nhất tôi đã làm?",
        ],
        "check_turn": 2,
        "expected_keyword": "Railway",
        "description": "Agent cần recall task 'deploy API lên Railway'",
    },

    # --- Group 4: Semantic Retrieval ---
    {
        "id": 7,
        "name": "Semantic Retrieval — Docker networking FAQ",
        "group": "semantic_retrieval",
        "turns": [
            "Làm sao để các container Docker nói chuyện với nhau?",
            "Cho tôi ví dụ cụ thể hơn về cách kết nối?",
        ],
        "check_turn": 0,
        "expected_keyword": "service name",
        "description": "Agent cần retrieve knowledge về Docker networking từ semantic memory",
    },
    {
        "id": 8,
        "name": "Semantic Retrieval — API Security",
        "group": "semantic_retrieval",
        "turns": [
            "Tôi cần bảo mật API của mình, nên làm gì?",
            "JWT là gì và dùng như thế nào?",
        ],
        "check_turn": 0,
        "expected_keyword": "JWT",
        "description": "Agent cần retrieve knowledge về API security từ semantic memory",
    },

    # --- Group 5: Token Budget / Trim ---
    {
        "id": 9,
        "name": "Token Budget — Conversation dài vẫn hoạt động",
        "group": "trim_token_budget",
        "turns": [
            "Tôi tên là Hùng.",
            "Tôi thích ăn phở.",
            "Tôi ở Đà Nẵng.",
            "Tôi học Machine Learning.",
            "Tôi dùng PyTorch.",
            "Tôi làm freelance.",
            "Tôi thích đọc sách.",
            "Tôi hay chạy bộ buổi sáng.",
            "Bạn có nhớ tên tôi và tôi ở đâu không?",
        ],
        "check_turn": 8,
        "expected_keyword": "Hùng",
        "description": "Agent vẫn nhớ thông tin quan trọng sau conversation dài (9 turns)",
    },
    {
        "id": 10,
        "name": "Combined — Profile + Semantic + Episodic",
        "group": "trim_token_budget",
        "turns": [
            "Tôi tên Anh, là dev Python.",
            "Hôm qua tôi lập trình xong feature authentication dùng JWT.",
            "Giờ tôi muốn tối ưu database, bạn có gợi ý gì dựa trên kinh nghiệm và kiến thức không?",
        ],
        "check_turn": 2,
        "expected_keyword": "index",
        "description": "Agent kết hợp profile (tên), episodic (JWT task), và semantic (DB optimization)",
    },
]


# ═══════════════════════════════════════════════════════════
# BENCHMARK RUNNER
# ═══════════════════════════════════════════════════════════

def run_single_scenario(scenario: dict, use_memory: bool) -> dict:
    """Run a single scenario and return results."""
    mode = "with-memory" if use_memory else "no-memory"
    
    # Create fresh agent for each scenario
    graph, memories, graph_config = create_agent(
        use_memory=use_memory,
        thread_id=f"bench_{scenario['id']}_{mode}",
    )

    # If with memory, ensure clean profile/episodic for fair test
    if use_memory:
        memories["long_term"].clear()
        memories["episodic"].clear()
        memories["short_term"].clear()

    responses = []
    for i, turn in enumerate(scenario["turns"]):
        try:
            response = run_agent_turn(graph, turn, graph_config)
            responses.append({"turn": i, "user": turn, "agent": response})
        except Exception as e:
            responses.append({"turn": i, "user": turn, "agent": f"[ERROR: {e}]"})

    # Check the critical turn for expected keyword
    check_idx = scenario["check_turn"]
    check_response = responses[check_idx]["agent"] if check_idx < len(responses) else ""
    passed = scenario["expected_keyword"].lower() in check_response.lower()

    return {
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "group": scenario["group"],
        "mode": mode,
        "responses": responses,
        "check_response": check_response,
        "expected_keyword": scenario["expected_keyword"],
        "passed": passed,
        "profile": memories["long_term"].get_profile() if use_memory else {},
    }


def run_benchmark():
    """Run full benchmark: all 10 scenarios × 2 modes."""
    print("=" * 70)
    print("🏋️  BENCHMARK: Multi-Memory Agent — 10 Multi-Turn Conversations")
    print("=" * 70)

    # Ensure knowledge base is seeded
    print("\n📚 Seeding knowledge base...")
    seed_knowledge_base()

    results = []

    for scenario in SCENARIOS:
        print(f"\n{'─' * 60}")
        print(f"📝 Scenario {scenario['id']}: {scenario['name']}")
        print(f"   Group: {scenario['group']}")
        print(f"   Turns: {len(scenario['turns'])}")
        print(f"   Expected: contains '{scenario['expected_keyword']}'")
        print(f"{'─' * 60}")

        # Run NO-MEMORY mode
        print(f"\n  🚫 No-memory mode...")
        no_mem_result = run_single_scenario(scenario, use_memory=False)
        results.append(no_mem_result)
        print(f"     Check response: {no_mem_result['check_response'][:100]}...")
        print(f"     {'✅ PASS' if no_mem_result['passed'] else '❌ FAIL'}")

        # Run WITH-MEMORY mode
        print(f"\n  🧠 With-memory mode...")
        mem_result = run_single_scenario(scenario, use_memory=True)
        results.append(mem_result)
        print(f"     Check response: {mem_result['check_response'][:100]}...")
        print(f"     {'✅ PASS' if mem_result['passed'] else '❌ FAIL'}")
        if mem_result.get("profile"):
            print(f"     Profile: {json.dumps(mem_result['profile'], ensure_ascii=False)[:100]}")

    # Generate summary
    print("\n" + "=" * 70)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 70)

    summary_table = []
    for scenario in SCENARIOS:
        no_mem = next(r for r in results if r["scenario_id"] == scenario["id"] and r["mode"] == "no-memory")
        with_mem = next(r for r in results if r["scenario_id"] == scenario["id"] and r["mode"] == "with-memory")

        no_mem_short = no_mem["check_response"][:60].replace("\n", " ")
        with_mem_short = with_mem["check_response"][:60].replace("\n", " ")

        summary_table.append({
            "id": scenario["id"],
            "name": scenario["name"],
            "group": scenario["group"],
            "no_memory_result": no_mem_short,
            "with_memory_result": with_mem_short,
            "no_memory_pass": no_mem["passed"],
            "with_memory_pass": with_mem["passed"],
        })

        status = "✅" if with_mem["passed"] else "❌"
        print(f"  {status} #{scenario['id']} {scenario['name']}")
        print(f"     No-mem: {'PASS' if no_mem['passed'] else 'FAIL'} | "
              f"With-mem: {'PASS' if with_mem['passed'] else 'FAIL'}")

    # Count passes
    no_mem_passes = sum(1 for s in summary_table if s["no_memory_pass"])
    with_mem_passes = sum(1 for s in summary_table if s["with_memory_pass"])
    print(f"\n  📈 No-memory:   {no_mem_passes}/10 passed")
    print(f"  📈 With-memory: {with_mem_passes}/10 passed")

    # Generate BENCHMARK.md
    generate_benchmark_md(summary_table, results)

    return results


def generate_benchmark_md(summary_table: list, full_results: list):
    """Generate BENCHMARK.md with results and reflection."""
    md_lines = []
    md_lines.append("# BENCHMARK — Multi-Memory Agent với LangGraph\n")
    md_lines.append(f"**Ngày chạy:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md_lines.append(f"**Model:** {config.MODEL_NAME}\n")
    md_lines.append(f"**Token Budget:** {config.MAX_TOKEN_BUDGET}\n")
    md_lines.append("")

    md_lines.append("---\n")
    md_lines.append("## Kết quả Benchmark — 10 Multi-Turn Conversations\n")
    md_lines.append("| # | Scenario | Group | No-memory result | With-memory result | Pass? |")
    md_lines.append("|---|----------|-------|------------------|---------------------|-------|")

    for s in summary_table:
        pass_str = "✅ Pass" if s["with_memory_pass"] else "❌ Fail"
        md_lines.append(
            f"| {s['id']} | {s['name']} | {s['group']} | "
            f"{s['no_memory_result'][:50]}... | "
            f"{s['with_memory_result'][:50]}... | "
            f"{pass_str} |"
        )

    no_mem_passes = sum(1 for s in summary_table if s["no_memory_pass"])
    with_mem_passes = sum(1 for s in summary_table if s["with_memory_pass"])
    md_lines.append(f"\n**Summary:** No-memory {no_mem_passes}/10 | With-memory {with_mem_passes}/10\n")

    # Detailed conversations
    md_lines.append("---\n")
    md_lines.append("## Chi tiết từng Conversation\n")

    for scenario in SCENARIOS:
        md_lines.append(f"### Scenario {scenario['id']}: {scenario['name']}\n")
        md_lines.append(f"**Group:** {scenario['group']}\n")
        md_lines.append(f"**Mô tả:** {scenario['description']}\n")
        md_lines.append(f"**Expected keyword:** `{scenario['expected_keyword']}`\n")

        for mode in ["no-memory", "with-memory"]:
            result = next(r for r in full_results if r["scenario_id"] == scenario["id"] and r["mode"] == mode)
            emoji = "🚫" if mode == "no-memory" else "🧠"
            md_lines.append(f"\n#### {emoji} {mode.title()}\n")
            for r in result["responses"]:
                md_lines.append(f"**User (turn {r['turn']+1}):** {r['user']}\n")
                md_lines.append(f"**Agent:** {r['agent'][:200]}{'...' if len(r['agent']) > 200 else ''}\n")

            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            md_lines.append(f"\n**Result:** {status}\n")
            if result.get("profile"):
                md_lines.append(f"**Profile state:** `{json.dumps(result['profile'], ensure_ascii=False)[:150]}`\n")

        md_lines.append("---\n")

    # Reflection section
    md_lines.append("## Reflection — Privacy & Limitations\n")
    md_lines.append("""
### 1. Memory nào giúp agent nhất?

**Long-term Profile Memory** giúp agent nhất vì cho phép cá nhân hóa mọi response.
Khi biết tên, nghề nghiệp, sở thích, dị ứng của user, agent có thể trả lời chính xác
và thân thiện hơn. **Semantic Memory** đứng thứ hai vì cung cấp knowledge factual
mà agent không thể tự biết.

### 2. Memory nào rủi ro nhất nếu retrieve sai?

**Long-term Profile Memory** rủi ro nhất:
- Nếu retrieve sai thông tin dị ứng → có thể gây nguy hiểm sức khỏe (khuyên ăn thứ user dị ứng)
- Thông tin cá nhân (tên, tuổi, nghề) nếu sai sẽ khiến user mất niềm tin
- PII (Personally Identifiable Information) stored dạng plaintext → risk nếu bị leak

**Episodic Memory** cũng rủi ro nếu ghi nhớ sai bài học → agent tái sử dụng kiến thức sai.

### 3. Nếu user yêu cầu xóa memory, xóa ở backend nào?

Cần xóa ở **tất cả backends**:
- **Short-term:** `clear()` — dễ nhất, chỉ là buffer trong RAM
- **Long-term Profile:** `delete_fact(key)` hoặc `clear()` — xóa file JSON
- **Episodic:** `delete_episode(id)` hoặc `clear()` — xóa file JSON
- **Semantic:** `delete_document(id)` hoặc `clear()` — xóa từ ChromaDB

Hiện tại system **chưa có cơ chế consent rõ ràng** (GDPR Right to be Forgotten).
Cần implement:
- Thông báo user trước khi lưu PII
- Cho phép user opt-out từng loại memory
- TTL (Time-To-Live) cho Profile facts — auto-expire sau N ngày
- Audit log cho mọi operation trên PII

### 4. Điều gì sẽ làm system fail khi scale?

**Limitations kỹ thuật:**

1. **JSON file-based storage** (Profile + Episodic): Không scale khi có nhiều users.
   Cần migrate sang Redis/PostgreSQL cho production.

2. **ChromaDB single-node**: Giới hạn khoảng 1M documents.
   Cần distributed vector DB (Pinecone, Weaviate) cho scale.

3. **LLM-based fact extraction**: Mỗi turn gọi thêm 1 lần LLM để extract facts
   → tăng latency và cost gấp đôi. Cần caching hoặc rule-based extraction cho facts đơn giản.

4. **Token budget**: Khi 4 loại memory đều lớn, trim có thể cắt mất thông tin quan trọng.
   Cần smarter prioritization (dùng relevance score thay vì order-based trim).

5. **Conflict detection**: Hoàn toàn phụ thuộc vào LLM → false positives/negatives.
   Cần hybrid approach: rule-based cho exact matches + LLM cho semantic conflicts.

6. **No encryption**: PII lưu plaintext trong JSON/ChromaDB.
   Production cần encryption at rest + in transit.

7. **Single-thread**: Không hỗ trợ concurrent users.
   Cần session management + per-user memory isolation.
""")

    # Write file
    benchmark_path = os.path.join(os.path.dirname(__file__), "BENCHMARK.md")
    with open(benchmark_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"\n📄 BENCHMARK.md đã được tạo: {benchmark_path}")


if __name__ == "__main__":
    run_benchmark()
