"""
Chat API Router for AI Chatbot Integration
Handles smart title generation, conversation history management, and secure user context injection.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
import logging
from pydantic import BaseModel
from src.models import Message, Conversation
from src.database import get_session_context
from src.agent.runner import agent_runner
from src.auth import get_current_user
from sqlmodel import select
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

# --- Pydantic Models for Request/Response ---

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

class GetConversationResponse(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]

# --- Endpoints ---

@router.post("/")
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    """
    Core Chat Endpoint:
    1. Authenticates user via JWT/Session.
    2. Injects the secure user_id into the AI Agent.
    3. Handles database persistence for messages and smart titles.
    """
    try:
        # SECURE CONTEXT: Get user ID from the authenticated session
        # This prevents the AI from needing to ask for a user_id
        user_id_str = str(current_user.id)

        # 1. Get AI Response with injected user context
        response_content = agent_runner.run_agent(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=user_id_str
        )

        with get_session_context() as session:
            # 2. Handle Conversation & Smart Title
            if request.conversation_id:
                stmt = select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == current_user.id
                )
                conversation = session.exec(stmt).first()
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")
            else:
                # SMART TITLE GENERATION: Take meaningful slice of first message
                raw_text = request.message.strip()
                if len(raw_text) > 40:
                    # Cut at last space before 40 chars to avoid partial words
                    title = raw_text[:40].rsplit(' ', 1)[0] + "..."
                else:
                    title = raw_text

                conversation = Conversation(user_id=current_user.id, title=title)
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

            # 3. Save Messages & Update Timestamp
            user_msg = Message(
                conversation_id=conversation.id,
                user_id=current_user.id,
                role="user",
                content=request.message
            )
            ai_msg = Message(
                conversation_id=conversation.id,
                user_id=current_user.id,
                role="assistant",
                content=response_content
            )

            # Ensure conversation moves to top of history
            conversation.updated_at = datetime.utcnow()

            session.add(user_msg)
            session.add(ai_msg)
            session.add(conversation)
            session.commit()
            session.refresh(user_msg)
            session.refresh(ai_msg)

            return {
                "conversation_id": conversation.id,
                "title": conversation.title,
                "message": response_content,
                "timestamp": datetime.utcnow().isoformat(),
                "user_message_id": user_msg.id,
                "assistant_message_id": ai_msg.id
            }
    except Exception as e:
        logger.error(f"Chat Error: {str(e)}")
        # Provide a descriptive error for debugging, then return 500
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/conversations")
async def list_conversations(current_user=Depends(get_current_user)):
    """List all conversations for the current authenticated user."""
    with get_session_context() as session:
        # Sort by updated_at so recent chats are always first
        stmt = select(Conversation).where(
            Conversation.user_id == current_user.id
        ).order_by(Conversation.updated_at.desc())

        conversations = session.exec(stmt).all()
        return [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat()
            } for c in conversations
        ]

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: int, current_user=Depends(get_current_user)):
    """Retrieve full message history for a specific conversation."""
    with get_session_context() as session:
        # Ownership verification
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        conversation = session.exec(stmt).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Fetch messages ordered by creation
        msg_stmt = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = session.exec(msg_stmt).all()

        return {
            "conversation": {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            },
            "messages": [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at.isoformat()
                } for m in messages
            ]
        }

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int, current_user=Depends(get_current_user)):
    """Delete a specific conversation and all its messages."""
    with get_session_context() as session:
        # Find the conversation and verify ownership
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        conversation = session.exec(stmt).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete all messages associated with this conversation first (due to foreign key constraint)
        msg_stmt = select(Message).where(Message.conversation_id == conversation_id)
        messages = session.exec(msg_stmt).all()
        for message in messages:
            session.delete(message)

        # Then delete the conversation itself
        session.delete(conversation)
        session.commit()

        return {"message": "Conversation deleted successfully"}