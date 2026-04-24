"""
Seed Knowledge Base: Populate semantic memory with knowledge documents.

Seeds ChromaDB with FAQ, coding tips, and domain knowledge
for the agent to retrieve via semantic search.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from memory.semantic import SemanticMemory
import config


KNOWLEDGE_DOCUMENTS = [
    {
        "id": "docker_networking",
        "text": "Trong Docker Compose, các container giao tiếp với nhau qua service name, "
                "không phải localhost. Ví dụ: nếu có service 'db', container khác connect "
                "bằng host 'db' thay vì 'localhost'. Port mapping (ports) chỉ dùng để expose "
                "ra host machine.",
        "metadata": {"source": "docker_tips", "category": "devops"},
    },
    {
        "id": "python_virtualenv",
        "text": "Luôn sử dụng virtual environment khi phát triển Python. Tạo venv bằng "
                "'python -m venv .venv', activate bằng '.venv/Scripts/activate' (Windows) "
                "hoặc 'source .venv/bin/activate' (Linux/Mac). Cài dependencies bằng "
                "'pip install -r requirements.txt'.",
        "metadata": {"source": "python_tips", "category": "development"},
    },
    {
        "id": "git_workflow",
        "text": "Git workflow chuẩn: tạo branch mới cho mỗi feature ('git checkout -b feature/name'), "
                "commit thường xuyên với message rõ ràng, push và tạo Pull Request. "
                "Không commit trực tiếp vào main/master. Dùng .gitignore để loại bỏ "
                "file nhạy cảm như .env, node_modules.",
        "metadata": {"source": "git_tips", "category": "development"},
    },
    {
        "id": "api_security",
        "text": "Bảo mật API: Luôn sử dụng HTTPS, implement JWT authentication, "
                "rate limiting (giới hạn request/phút), validate input data, "
                "không expose sensitive info trong error messages. "
                "Sử dụng environment variables cho API keys, không hardcode.",
        "metadata": {"source": "security_tips", "category": "security"},
    },
    {
        "id": "database_optimization",
        "text": "Tối ưu database: Sử dụng index cho các cột thường query, "
                "tránh SELECT *, dùng connection pooling, implement caching "
                "cho data ít thay đổi. PostgreSQL hỗ trợ EXPLAIN ANALYZE "
                "để phân tích query performance.",
        "metadata": {"source": "database_tips", "category": "database"},
    },
    {
        "id": "error_handling",
        "text": "Best practices xử lý lỗi trong Python: Dùng try/except cụ thể "
                "(không catch Exception chung), log error với traceback đầy đủ, "
                "implement retry logic cho network calls, sử dụng custom exceptions "
                "cho business logic errors.",
        "metadata": {"source": "python_tips", "category": "development"},
    },
    {
        "id": "memory_systems",
        "text": "Hệ thống memory cho AI Agent gồm 4 loại: Short-term (buffer hội thoại gần), "
                "Long-term Profile (thông tin user dài hạn), Episodic (các sự kiện/bài học), "
                "và Semantic (knowledge base vector search). Mỗi loại có backend riêng "
                "và vai trò khác nhau trong việc cá nhân hóa agent.",
        "metadata": {"source": "ai_knowledge", "category": "ai"},
    },
    {
        "id": "langraph_patterns",
        "text": "LangGraph sử dụng StateGraph pattern: define state bằng TypedDict, "
                "thêm node (functions), nối bằng edges. Conditional edges cho phép "
                "routing logic. Checkpointer (MemorySaver) lưu state giữa các lần gọi. "
                "Mỗi node nhận state và trả về partial update.",
        "metadata": {"source": "ai_knowledge", "category": "ai"},
    },
    {
        "id": "testing_strategy",
        "text": "Chiến lược testing: Unit test cho functions riêng lẻ (pytest), "
                "integration test cho API endpoints, end-to-end test cho user flows. "
                "Aim cho 80% code coverage. Mock external services trong unit tests. "
                "Dùng fixtures cho test data.",
        "metadata": {"source": "testing_tips", "category": "development"},
    },
    {
        "id": "deployment_checklist",
        "text": "Checklist deploy production: Health check endpoint (/health), "
                "environment variables configuration, logging setup (structured JSON), "
                "monitoring & alerting, graceful shutdown handling, "
                "database migration strategy, rollback plan.",
        "metadata": {"source": "devops_tips", "category": "devops"},
    },
    {
        "id": "chromadb_usage",
        "text": "ChromaDB là vector database open-source. Sử dụng PersistentClient "
                "để lưu data trên disk. Hỗ trợ cosine similarity mặc định. "
                "Query bằng query_texts, trả về documents + distances. "
                "Embedding tự động bằng all-MiniLM-L6-v2.",
        "metadata": {"source": "ai_knowledge", "category": "ai"},
    },
    {
        "id": "vietnam_food_allergies",
        "text": "Các dị ứng thực phẩm phổ biến ở Việt Nam: đậu phộng (lạc), "
                "hải sản (tôm, cua, cá), sữa bò, đậu nành, gluten (lúa mì). "
                "Khi nấu ăn cho người dị ứng, cần kiểm tra kỹ thành phần "
                "và tránh cross-contamination.",
        "metadata": {"source": "health_knowledge", "category": "health"},
    },
]


def seed_knowledge_base():
    """Seed the semantic memory with knowledge documents."""
    print("🌱 Seeding knowledge base...")
    
    semantic = SemanticMemory(
        persist_directory=config.CHROMA_DB_PATH,
        collection_name=config.SEMANTIC_COLLECTION_NAME,
    )

    # Clear existing data
    semantic.clear()

    # Add documents
    texts = [doc["text"] for doc in KNOWLEDGE_DOCUMENTS]
    ids = [doc["id"] for doc in KNOWLEDGE_DOCUMENTS]
    metadatas = [doc["metadata"] for doc in KNOWLEDGE_DOCUMENTS]

    semantic.add_documents_batch(texts=texts, doc_ids=ids, metadatas=metadatas)

    print(f"✅ Seeded {semantic.count} documents into knowledge base")
    print(f"📂 Stored at: {config.CHROMA_DB_PATH}")

    # Test search
    print("\n🔍 Test search: 'Docker networking'")
    results = semantic.search("Docker networking giữa các container", n_results=2)
    for r in results:
        print(f"  → [{r['distance']:.4f}] {r['document'][:80]}...")

    print("\n🔍 Test search: 'dị ứng thực phẩm'")
    results = semantic.search("dị ứng thực phẩm", n_results=2)
    for r in results:
        print(f"  → [{r['distance']:.4f}] {r['document'][:80]}...")

    return semantic


if __name__ == "__main__":
    seed_knowledge_base()
