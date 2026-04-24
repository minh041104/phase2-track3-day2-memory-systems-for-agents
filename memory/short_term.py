"""
Short-term Memory: Sliding window conversation buffer.

Backend: Python list (in-memory).
Role: Giữ N tin nhắn gần nhất để cung cấp context ngắn hạn cho agent.
"""
from __future__ import annotations
from typing import Any


class ShortTermMemory:
    """Sliding window buffer giữ N messages gần nhất."""

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self._buffer: list[dict[str, str]] = []

    # ── Public API ────────────────────────────────────

    def add_message(self, role: str, content: str) -> None:
        """Thêm message vào buffer, tự động trim nếu vượt quá window."""
        self._buffer.append({"role": role, "content": content})
        # Trim: giữ window_size cặp messages (mỗi cặp = 1 user + 1 assistant)
        if len(self._buffer) > self.window_size * 2:
            self._buffer = self._buffer[-(self.window_size * 2):]

    def get_recent(self, n: int | None = None) -> list[dict[str, str]]:
        """Trả về n messages gần nhất. None = toàn bộ buffer."""
        if n is None:
            return list(self._buffer)
        return list(self._buffer[-n:])

    def clear(self) -> None:
        """Xóa toàn bộ buffer."""
        self._buffer.clear()

    def format_for_prompt(self) -> str:
        """Format buffer thành chuỗi để inject vào prompt."""
        if not self._buffer:
            return "Không có cuộc hội thoại gần đây."
        lines = []
        for msg in self._buffer:
            role_label = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role_label}: {msg['content']}")
        return "\n".join(lines)

    @property
    def size(self) -> int:
        return len(self._buffer)

    def __repr__(self) -> str:
        return f"ShortTermMemory(window={self.window_size}, current={self.size})"
