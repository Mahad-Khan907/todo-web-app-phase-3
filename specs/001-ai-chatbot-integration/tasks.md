# Task List: AI Chatbot Integration with MCP and OpenAI Agents

**Feature**: AI Chatbot with MCP | **Branch**: `001-ai-chatbot-integration`
**ID Strategy**: Sequential Integers (1, 2, 3...) | **Skill Usage**: Dynamic

## Implementation Strategy

This feature will be implemented in priority order of user stories, with each story being independently testable. The core functionality (US1) will be delivered first as an MVP, followed by conversation context management (US2), and finally security enhancements (US3).

## Phase 1: Setup (Project Initialization)

### Goal
Initialize the project structure and ensure all dependencies are available for the AI Chatbot implementation.

- [ ] T001 Set up backend directory structure: `src/mcp/`, `src/agent/`, `src/routers/chat.py`
- [ ] T002 Set up frontend directory structure: `frontend/src/components/chat/`
- [ ] T003 [P] Install required dependencies: `openai`, `uv` package for MCP SDK
- [ ] T004 [P] Verify existing authentication system is accessible for chat endpoint protection

## Phase 2: Foundational (Blocking Prerequisites)

### Goal
Establish the foundational components that all user stories depend on.

- [X] T005 Update `Task` model in `backend/src/models.py` to use sequential integer ID (PK, Autoincrement)
- [X] T006 Add `Conversation` and `Message` models with sequential integer Primary Keys to `backend/src/models.py`
- [X] T007 [P] Create database migration for new models using Alembic
- [X] T008 [P] [Skill Trigger] Run `.claude/skills/validate_models` to ensure SQLModel relationships and Integer sequences are correctly mapped
- [X] T009 [Skill Trigger] Run `.claude/skills/lint_check` on the updated models to ensure code quality
- [X] T010 Create MCP server foundation in `backend/src/mcp/server.py`

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

### Goal
Enable users to interact with their todo list using natural language commands to add, list, complete, update, and delete tasks.

### Independent Test Criteria
User can add, list, complete, update, and delete tasks using natural language commands like "Add a task to buy groceries", "Show me my tasks", "Mark task 3 as complete", etc.

- [X] T011 [P] [US1] Implement `add_task` MCP tool in `backend/src/mcp/server.py` with integer ID return
- [X] T012 [P] [US1] Implement `list_tasks` MCP tool in `backend/src/mcp/server.py` returning tasks with integer IDs
- [X] T013 [US1] Implement `complete_task` MCP tool in `backend/src/mcp/server.py` accepting integer task ID
- [X] T014 [P] [US1] Implement `update_task` MCP tool in `backend/src/mcp/server.py` accepting integer task ID
- [X] T015 [US1] Implement `delete_task` MCP tool in `backend/src/mcp/server.py` accepting integer task ID
- [X] T016 [US1] Create OpenAI Agent runner in `backend/src/agent/runner.py`
- [X] T017 [US1] Connect MCP tools to the OpenAI Agent in the runner
- [X] T018 [US1] Create `POST /api/chat` endpoint in `backend/src/routers/chat.py` with basic functionality
- [X] T019 [P] [US1] Implement frontend ChatInterface component in `frontend/src/components/chat/ChatInterface.tsx`
- [X] T020 [P] [US1] Integrate ChatInterface into dashboard page at `frontend/src/app/dashboard/page.tsx`
- [X] T021 [US1] [Skill Trigger] Run `.claude/skills/test_runner` to verify tool calls work correctly
- [X] T022 [US1] [Skill Trigger] Run `.claude/skills/lint_check` on new backend modules

### Acceptance Scenarios
1. User can add a task with natural language and see it appear with a sequential integer ID
2. User can list tasks and see them with sequential integer IDs
3. User can complete a task by referencing its integer ID

## Phase 4: User Story 2 - Conversation Context Management (Priority: P2)

### Goal
Enable the AI to maintain context across multiple interactions within a conversation.

### Independent Test Criteria
User can have a multi-turn conversation where the AI remembers the context and can reference previous interactions and tasks.

- [X] T023 [P] [US2] Enhance `Message` model to support conversation context storage
- [X] T024 [US2] Implement logic to fetch conversation context from DB in `backend/src/agent/runner.py`
- [X] T025 [US2] Update chat endpoint to manage conversation state using conversation_id
- [X] T026 [P] [US2] Implement conversation history retrieval in the agent runner
- [X] T027 [US2] Add conversation title auto-generation based on content
- [X] T028 [US2] Update frontend to maintain conversation context across messages
- [X] T029 [US2] [Skill Trigger] Test multi-turn conversation functionality

### Acceptance Scenarios
1. AI remembers context from previous interactions in the same conversation
2. User can switch between multiple conversations and each maintains its own context

## Phase 5: User Story 3 - Secure Task Access (Priority: P3)

### Goal
Ensure that only authenticated users can access and modify their own tasks through the AI chatbot.

### Independent Test Criteria
User can only see and modify their own tasks, and the AI respects user authentication boundaries.

- [X] T030 [US3] Update chat endpoint to extract and verify user_id from JWT token
- [X] T031 [P] [US3] Implement user_id validation in all MCP tools to ensure proper task ownership
- [X] T032 [US3] Add user_id validation to conversation creation and access
- [X] T033 [P] [US3] Implement proper user isolation in list_tasks to only return user's tasks
- [X] T034 [US3] Add authentication middleware verification for chat endpoint
- [X] T035 [US3] [Skill Trigger] Test that users cannot access other users' tasks
- [X] T036 [US3] [Skill Trigger] Test that unauthenticated users are prompted to log in

### Acceptance Scenarios
1. Authenticated user can only see and modify their own tasks
2. Unauthenticated users are prompted to log in before accessing the chatbot

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Add error handling, edge case management, and finalize the UI/UX.

- [X] T037 [P] Add comprehensive error handling for MCP tools
- [X] T038 Handle edge case: task ID that doesn't exist in tool calls
- [X] T039 [P] Handle edge case: malformed natural language requests
- [X] T040 Add retry logic for when AI service is temporarily unavailable
- [X] T041 [P] Implement proper message streaming in frontend for better UX
- [X] T042 Add loading states and error messages to ChatInterface
- [X] T043 [P] Style chat interface to match existing dashboard theme with Tailwind CSS
- [X] T044 [P] [Skill Trigger] Run comprehensive linting on all new files
- [X] T045 [Skill Trigger] Run full integration tests to verify concurrent UI and AI modifications work correctly

## Dependencies

- US2 (Conversation Context) depends on US1 (Task Management) foundational components
- US3 (Security) can be implemented in parallel with US1 and US2 since it adds validation layers

## Parallel Execution Opportunities

- Backend MCP tools (T011-T015) can be developed in parallel [P]
- Frontend components (T019) can be developed in parallel with backend API [P]
- Model validation (T008) and linting (T009) can run in parallel [P]
- Multiple conversation context features (T023, T025) can be developed in parallel [P]
- Security validations (T031, T033) can be implemented in parallel [P]