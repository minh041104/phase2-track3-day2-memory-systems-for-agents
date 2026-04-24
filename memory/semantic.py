"""
Semantic Memory: ChromaDB vector search for knowledge base.

Backend: ChromaDB PersistentClient.
Role: Lưu trữ và truy xuất knowledge chunks dựa trên semantic similarity.
      Dùng cho FAQ, coding tips, domain knowledge, v.v.
"""
from __future__ import annotations

from typing import Any

import chromadb
from chromadb.config import Settings


class SemanticMemory:
    """ChromaDB-based vector search for semantic knowledge retrieval."""

    def __init__(self, persist_directory: str, collection_name: str = "knowledge_base"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Initialize ChromaDB persistent client
        self._client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},  # cosine similarity
        )

    # ── Public API ────────────────────────────────────

    def add_document(
        self,
        text: str,
        doc_id: str | None = None,
        metadata: dict | None = None,
    ) -> str:
        """
        Thêm một document vào knowledge base.
        
        Args:
            text: Nội dung document
            doc_id: ID tuỳ chọn (auto-generate nếu None)
            metadata: Metadata bổ sung (source, category, v.v.)
            
        Returns:
            Document ID.
        """
        import uuid
        if doc_id is None:
            doc_id = f"doc_{uuid.uuid4().hex[:8]}"

        self._collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[metadata or {}],
        )
        return doc_id

    def add_documents_batch(
        self,
        texts: list[str],
        doc_ids: list[str] | None = None,
        metadatas: list[dict] | None = None,
    ) -> list[str]:
        """Thêm nhiều documents cùng lúc."""
        import uuid
        if doc_ids is None:
            doc_ids = [f"doc_{uuid.uuid4().hex[:8]}" for _ in texts]
        if metadatas is None:
            metadatas = [{}] * len(texts)

        self._collection.add(
            documents=texts,
            ids=doc_ids,
            metadatas=metadatas,
        )
        return doc_ids

    def search(self, query: str, n_results: int = 3) -> list[dict]:
        """
        Tìm kiếm semantic trong knowledge base.
        
        Args:
            query: Câu truy vấn
            n_results: Số kết quả trả về
            
        Returns:
            List of dicts với keys: document, metadata, distance
        """
        # Ensure we don't request more than available
        total = self._collection.count()
        if total == 0:
            return []
        n_results = min(n_results, total)

        results = self._collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        hits = []
        if results and results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                hit = {
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None,
                }
                hits.append(hit)
        return hits

    def delete_document(self, doc_id: str) -> None:
        """Xóa document theo ID."""
        self._collection.delete(ids=[doc_id])

    def clear(self) -> None:
        """Xóa toàn bộ collection và tạo lại."""
        self._client.delete_collection(self.collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def format_for_prompt(self, query: str, n_results: int = 3) -> str:
        """Search và format kết quả thành chuỗi để inject vào prompt."""
        hits = self.search(query, n_results)
        if not hits:
            return "Không tìm thấy thông tin liên quan trong knowledge base."
        lines = []
        for i, hit in enumerate(hits, 1):
            source = hit["metadata"].get("source", "unknown")
            lines.append(f"[{i}] (source: {source}) {hit['document']}")
        return "\n".join(lines)

    @property
    def count(self) -> int:
        return self._collection.count()

    def __repr__(self) -> str:
        return f"SemanticMemory(collection='{self.collection_name}', docs={self.count})"
