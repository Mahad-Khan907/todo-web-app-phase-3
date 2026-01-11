# Quickstart Guide: AI Chatbot Integration

## Prerequisites
- Python 3.13+
- Node.js 18+
- uv package manager
- PostgreSQL database (Neon recommended)
- OpenAI API key

## Setup

### 1. Environment Configuration
```bash
# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export DATABASE_URL="your-postgres-connection-string"
export SECRET_KEY="your-jwt-secret-key"
```

### 2. Backend Setup
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run database migrations to create extended models
uv run alembic upgrade head
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Running the Application

### 1. Start Backend Server
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

### 2. Access the Application
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Chat Endpoint: POST http://localhost:8000/api/chat

## Using the Chat Feature

### 1. Authentication
- Login to the dashboard using existing auth system
- JWT token will be automatically used for chat requests

### 2. Starting a Conversation
- Navigate to the dashboard
- Type messages in the chat interface
- AI will respond and can perform task operations

### 3. Natural Language Commands
Examples:
- "Add a task to buy groceries" → Creates new task
- "Show me my tasks" → Lists all current tasks
- "Mark task 3 as complete" → Completes task with ID 3
- "Update task 2 to 'buy milk'" → Updates task title
- "Delete task 1" → Removes task with ID 1

## Development

### Backend Structure
- `src/models.py` - Extended data models with Conversation and Message
- `src/mcp/server.py` - MCP tools implementation
- `src/agent/runner.py` - OpenAI Agent logic
- `src/routers/chat.py` - Chat API endpoint

### Frontend Structure
- `frontend/src/app/dashboard/page.tsx` - Dashboard with chat integration
- `frontend/src/components/chat/ChatInterface.tsx` - Chat UI component

## Testing
```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd frontend
npm test
```