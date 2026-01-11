---
name: Chatbot DB Models
description: Reusable SQLModel database models for chatbot conversations and messages with proper relationships and constraints.
model: sonnet
---

Reusable Skill:

Skill: Chatbot Database Models – Input: Model requirements including relationships, constraints, and indexing needs; Output: Full SQLModel Conversation and Message models with proper foreign keys, indexing, validation schemas, and Neon PostgreSQL compatibility.

Usage Example:
```python
# Realistic example of chatbot database models
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    title: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default=None, primary_key=True)
    conversation_id: str = Field(index=True, foreign_key="conversations.id")
    user_id: str = Field(index=True, foreign_key="users.id")
    role: str = Field(regex="^(user|assistant|system)$")  # Enum equivalent
    content: str = Field(sa_column_kwargs={"nullable": False})
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")

# Pydantic schemas for API validation
from pydantic import BaseModel

class ConversationCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    role: str
    content: str
```

Notes:

These models include proper indexing for performance, foreign key relationships for data integrity, appropriate constraints for data validation, and are optimized for Neon PostgreSQL. The models support efficient querying of conversation history and proper user-specific data isolation.