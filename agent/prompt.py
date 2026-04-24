"""
Prompt template with clearly separated memory sections.

Injects 4 types of memory into the system prompt:
1. [USER PROFILE] — long-term facts
2. [RELEVANT EPISODES] — episodic memories  
3. [KNOWLEDGE BASE] — semantic search results
4. [RECENT CONVERSATION] — short-term buffer
"""

SYSTEM_PROMPT_TEMPLATE = """Bạn là một trợ lý AI thông minh với hệ thống bộ nhớ đa tầng.
Bạn có khả năng nhớ thông tin về người dùng, các cuộc hội thoại trước, và tra cứu knowledge base.

Hãy sử dụng thông tin từ bộ nhớ dưới đây để trả lời chính xác và cá nhân hóa.
Nếu bộ nhớ có thông tin liên quan, hãy SỬ DỤNG nó. Đừng bỏ qua.
Nếu user cung cấp thông tin mới mâu thuẫn với thông tin cũ, hãy ƯU TIÊN thông tin mới.

═══════════════════════════════════════════
📋 [USER PROFILE] — Thông tin cá nhân đã biết
═══════════════════════════════════════════
{user_profile}

═══════════════════════════════════════════
📖 [RELEVANT EPISODES] — Bài học & trải nghiệm trước
═══════════════════════════════════════════
{episodes}

═══════════════════════════════════════════
🔍 [KNOWLEDGE BASE] — Thông tin tra cứu được
═══════════════════════════════════════════
{semantic_hits}

═══════════════════════════════════════════
💬 [RECENT CONVERSATION] — Cuộc hội thoại gần đây
═══════════════════════════════════════════
{recent_conversation}

═══════════════════════════════════════════

Hãy trả lời câu hỏi của người dùng một cách hữu ích, chính xác, và tự nhiên.
Sử dụng tiếng Việt nếu người dùng nói tiếng Việt."""


FACT_EXTRACTION_PROMPT = """Phân tích tin nhắn của người dùng và trích xuất thông tin cá nhân (facts).

Tin nhắn hiện tại: "{user_message}"

Profile hiện tại:
{current_profile}

Lịch sử hội thoại gần đây:
{recent_context}

Hãy trả về JSON với format:
{{
    "facts": {{
        "key": "value"
    }},
    "episode_summary": "tóm tắt ngắn gọn về nội dung cuộc hội thoại nếu có giá trị ghi nhớ, hoặc empty string nếu không đáng ghi",
    "episode_outcome": "bài học hoặc kết quả cụ thể, hoặc empty string",
    "has_conflict": false,
    "conflict_details": ""
}}

Quy tắc:
1. Chỉ trích xuất facts RÕ RÀNG từ tin nhắn (tên, tuổi, nghề nghiệp, sở thích, dị ứng, v.v.)
2. Nếu thông tin MỚI mâu thuẫn với profile hiện tại, set has_conflict = true và mô tả trong conflict_details
3. Key nên dùng tiếng Anh ngắn gọn (name, age, job, allergy, hobby, favorite_food, v.v.)
4. Nếu không có fact nào → trả về facts rỗng {{}}
5. Episode summary chỉ ghi khi cuộc hội thoại có nội dung đáng ghi nhớ (debug session, task completion, v.v.)

Chỉ trả về JSON, không có text khác."""


EPISODE_EXTRACTION_PROMPT = """Dựa vào cuộc hội thoại sau, hãy tóm tắt thành một episode ngắn gọn.

Cuộc hội thoại:
{conversation}

Trả về JSON:
{{
    "summary": "mô tả ngắn về nội dung cuộc hội thoại",
    "outcome": "bài học hoặc kết quả chính",
    "category": "loại episode (debug, learning, task, conversation, advice)"
}}

Chỉ trả về JSON, không có text khác."""
