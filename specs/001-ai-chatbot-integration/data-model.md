# Data Model: AI Chatbot Integration

## Entity: Task
**Description**: Represents a user's todo item
- `id`: int (Primary Key, Auto-incrementing) - Sequential integer ID
- `title`: str - Task description/title
- `description`: str (Optional) - Additional details about the task
- `completed`: bool - Whether the task is completed
- `user_id`: str - Foreign key reference to the user who owns this task
- `created_at`: datetime - Timestamp when task was created
- `updated_at`: datetime - Timestamp when task was last updated

## Entity: Conversation
**Description**: Represents a session of interaction between user and AI
- `id`: int (Primary Key, Auto-incrementing) - Sequential integer ID
- `user_id`: str - Foreign key reference to the user who owns this conversation
- `title`: str (Optional) - Auto-generated title based on conversation content
- `created_at`: datetime - Timestamp when conversation was started
- `updated_at`: datetime - Timestamp when conversation was last updated

## Entity: Message
**Description**: Represents a single exchange within a conversation
- `id`: int (Primary Key, Auto-incrementing) - Sequential integer ID
- `conversation_id`: int - Foreign key reference to the conversation this message belongs to
- `user_id`: str - Foreign key reference to the user who sent this message
- `role`: str - Either "user" or "assistant"
- `content`: str - The actual message content
- `created_at`: datetime - Timestamp when message was created

## Relationships
- Task belongs to User (via user_id foreign key)
- Conversation belongs to User (via user_id foreign key)
- Message belongs to Conversation (via conversation_id foreign key)
- Message belongs to User (via user_id foreign key)

## Validation Rules
- Task.user_id must match authenticated user for any operation
- Conversation.user_id must match authenticated user for any operation
- Message.user_id must match authenticated user for creating messages
- Message.conversation_id must reference an existing conversation that belongs to the same user

## State Transitions
- Task: `completed` field can transition from False to True (complete) or True to False (uncomplete)
- Message: Immutable after creation (no state changes allowed)

## Constraints
- All user-specific data must be properly isolated by user_id
- Task and Conversation IDs must be sequential integers starting from 1
- Message role must be either "user" or "assistant"