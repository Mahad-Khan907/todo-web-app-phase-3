---
name: Conversation Persistence
description: Reusable conversation history storage and retrieval with user-specific data isolation and efficient querying.
model: sonnet
---

Reusable Skill:

Skill: Conversation Persistence – Input: User context, conversation data, and query parameters; Output: Full conversation and message persistence implementation with SQLModel, user-specific filtering, efficient querying, and pagination support.

Usage Example:
```python
# Realistic example of conversation persistence
from sqlmodel import SQLModel, Field, Relationship, select
from typing import Optional, List
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    conversation: Conversation = Relationship(back_populates="messages")

async def store_conversation(user_id: str, user_message: str, ai_response: str):
    conversation = Conversation(user_id=user_id, title=user_message[:50])
    # ... save to database
```

Notes:

These models provide proper user-specific data isolation, efficient indexing for queries, foreign key relationships, and support for conversation history retrieval. Includes proper timestamping, role-based message tracking, and pagination support for large conversation histories.