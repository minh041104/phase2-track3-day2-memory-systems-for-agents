"""
Episodic Memory: JSON log store for task outcomes and lessons learned.

Backend: JSON file.
Role: Lưu trữ các "episodes" — tóm tắt các task đã hoàn thành,
      bài học rút ra, lỗi đã gặp, v.v. để agent có thể recall sau này.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any


class EpisodicMemory:
    """JSON log store for episodic memories (task outcomes, lessons)."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._episodes: list[dict[str, Any]] = []
        self._load()

    # ── Persistence ───────────────────────────────────

    def _load(self) -> None:
        """Load episodes từ JSON file."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self._episodes = json.load(f)

    def _save(self) -> None:
        """Persist episodes ra JSON file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._episodes, f, ensure_ascii=False, indent=2)

    # ── Public API ────────────────────────────────────

    def add_episode(
        self,
        summary: str,
        outcome: str,
        category: str = "general",
        metadata: dict | None = None,
    ) -> dict:
        """
        Ghi một episode mới.
        
        Args:
            summary: Mô tả ngắn gọn episode (ví dụ: "User hỏi về Docker networking")
            outcome: Kết quả/bài học (ví dụ: "Dùng docker service name thay vì localhost")
            category: Phân loại episode
            metadata: Thông tin bổ sung tuỳ ý
            
        Returns:
            Episode dict đã được lưu.
        """
        episode = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": summary,
            "outcome": outcome,
            "category": category,
            "metadata": metadata or {},
        }
        self._episodes.append(episode)
        self._save()
        return episode

    def get_recent_episodes(self, n: int = 5) -> list[dict]:
        """Trả về n episodes gần nhất."""
        return list(self._episodes[-n:])

    def get_all_episodes(self) -> list[dict]:
        """Trả về toàn bộ episodes."""
        return list(self._episodes)

    def search_episodes(self, keyword: str) -> list[dict]:
        """Tìm episodes chứa keyword trong summary hoặc outcome."""
        keyword_lower = keyword.lower()
        results = []
        for ep in self._episodes:
            if (keyword_lower in ep.get("summary", "").lower() or
                keyword_lower in ep.get("outcome", "").lower()):
                results.append(ep)
        return results

    def delete_episode(self, episode_id: str) -> bool:
        """Xóa episode theo ID."""
        for i, ep in enumerate(self._episodes):
            if ep.get("id") == episode_id:
                self._episodes.pop(i)
                self._save()
                return True
        return False

    def clear(self) -> None:
        """Xóa toàn bộ episodes."""
        self._episodes.clear()
        self._save()

    def format_for_prompt(self, n: int = 5) -> str:
        """Format episodes gần nhất thành chuỗi để inject vào prompt."""
        recent = self.get_recent_episodes(n)
        if not recent:
            return "Chưa có episode nào được ghi nhận."
        lines = []
        for ep in recent:
            lines.append(
                f"- [{ep.get('category', 'general')}] {ep['summary']}\n"
                f"  Kết quả: {ep['outcome']}"
            )
        return "\n".join(lines)

    @property
    def count(self) -> int:
        return len(self._episodes)

    def __repr__(self) -> str:
        return f"EpisodicMemory(episodes={self.count})"
