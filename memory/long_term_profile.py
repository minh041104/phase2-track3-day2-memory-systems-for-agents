"""
Long-term Profile Memory: JSON-based Key-Value store for user facts.

Backend: JSON file.
Role: Lưu trữ thông tin cá nhân của user (tên, sở thích, dị ứng, v.v.)
      với khả năng conflict handling — fact mới override fact cũ.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any


class LongTermProfileMemory:
    """JSON-based KV store for user profile facts with conflict handling."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._profile: dict[str, Any] = {}
        self._change_log: list[dict] = []  # track changes for auditability
        self._load()

    # ── Persistence ───────────────────────────────────

    def _load(self) -> None:
        """Load profile từ JSON file."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._profile = data.get("profile", {})
                self._change_log = data.get("change_log", [])

    def _save(self) -> None:
        """Persist profile ra JSON file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(
                {"profile": self._profile, "change_log": self._change_log},
                f,
                ensure_ascii=False,
                indent=2,
            )

    # ── Public API ────────────────────────────────────

    def get_profile(self) -> dict[str, Any]:
        """Trả về toàn bộ profile."""
        return dict(self._profile)

    def get_fact(self, key: str) -> Any | None:
        """Lấy một fact cụ thể."""
        return self._profile.get(key)

    def update_fact(self, key: str, value: Any) -> dict:
        """
        Update hoặc thêm mới một fact.
        Nếu key đã tồn tại với value khác → conflict handling:
        - Overwrite với value mới
        - Log change vào change_log
        
        Returns dict mô tả hành động đã thực hiện.
        """
        old_value = self._profile.get(key)
        action = "created"

        if old_value is not None and old_value != value:
            action = "updated (conflict resolved)"
            # Log the conflict resolution
            self._change_log.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "key": key,
                "old_value": old_value,
                "new_value": value,
                "action": "conflict_resolved",
            })
        elif old_value == value:
            return {"action": "no_change", "key": key, "value": value}

        self._profile[key] = value
        self._save()

        return {"action": action, "key": key, "old_value": old_value, "new_value": value}

    def update_facts(self, facts: dict[str, Any]) -> list[dict]:
        """Update nhiều facts cùng lúc. Returns list các actions."""
        results = []
        for key, value in facts.items():
            result = self.update_fact(key, value)
            results.append(result)
        return results

    def delete_fact(self, key: str) -> bool:
        """Xóa một fact. Returns True nếu đã xóa."""
        if key in self._profile:
            old_value = self._profile.pop(key)
            self._change_log.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "key": key,
                "old_value": old_value,
                "action": "deleted",
            })
            self._save()
            return True
        return False

    def get_all_facts(self) -> dict[str, Any]:
        """Alias cho get_profile()."""
        return self.get_profile()

    def get_change_log(self) -> list[dict]:
        """Trả về lịch sử thay đổi."""
        return list(self._change_log)

    def clear(self) -> None:
        """Xóa toàn bộ profile và change log."""
        self._profile.clear()
        self._change_log.clear()
        self._save()

    def format_for_prompt(self) -> str:
        """Format profile thành chuỗi để inject vào prompt."""
        if not self._profile:
            return "Chưa có thông tin profile nào."
        lines = []
        for key, value in self._profile.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"LongTermProfileMemory(facts={len(self._profile)})"
