from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
import uuid
from sqlalchemy import Column
from sqlalchemy.types import JSON

if TYPE_CHECKING:
    pass


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, table=True):
    """
    User model representing a registered user with authentication credentials.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class UserPublic(UserBase):
    """
    Schema for returning user data (without sensitive information).
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Task(TaskBase, table=True):
    """
    Task model representing a todo item that belongs to a specific user.
    """
    id: int = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    tags: List[str] = Field(default_factory=list)


class TaskUpdate(SQLModel):
    """
    Schema for updating a task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskPublic(TaskBase):
    """
    Schema for returning task data.
    """
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)


class ConversationBase(SQLModel):
    user_id: uuid.UUID
    title: Optional[str] = None


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a session of interaction between user and AI.
    """
    id: int = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    """
    Schema for creating a new conversation.
    """
    pass


class ConversationPublic(ConversationBase):
    """
    Schema for returning conversation data.
    """
    id: int
    created_at: datetime
    updated_at: datetime


class MessageBase(SQLModel):
    conversation_id: int
    user_id: uuid.UUID
    role: str  # "user" or "assistant"
    content: str


class Message(MessageBase, table=True):
    """
    Message model representing a single exchange within a conversation.
    """
    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    role: str = Field(regex="^(user|assistant)$")  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """
    Schema for creating a new message.
    """
    pass


class MessagePublic(MessageBase):
    id: int
    created_at: datetime


from pydantic import root_validator

class TaskBulkUpdateItem(SQLModel):
    """
    Schema for a single item in a bulk task update request.
    Identifies a task by its ID or title and provides fields to update.
    """
    id: Optional[int] = None
    title: Optional[str] = None
    updates: TaskUpdate

    @root_validator(pre=True)
    def check_id_or_title(cls, values):
        if values.get("id") is None and values.get("title") is None:
            raise ValueError("Either 'id' or 'title' must be provided for a bulk update item.")
        return values

class TaskBulkUpdateResult(SQLModel):
    """
    Schema for the result of a single bulk task update operation.
    """
    identifier: Optional[str] = None  # Original identifier (id or title string representation)
    status: str  # "success", "failed", "ambiguous"
    message: Optional[str] = None
    task: Optional[TaskPublic] = None # The updated task if successful

class TaskBulkUpdateResponse(SQLModel):
    """
    Schema for the overall response of a bulk task update request.
    """
    results: List[TaskBulkUpdateResult]

