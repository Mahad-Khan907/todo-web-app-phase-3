# Implementation Plan: AI Chatbot Integration

**Branch**: `001-ai-chatbot-integration` | **Date**: 2026-01-06 | **Spec**: [AI Chatbot Integration Spec](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan integrates an AI Chatbot into the existing Todo App using OpenAI Agents SDK and MCP (Model Context Protocol). The implementation follows a stateless architecture where all conversation state is persisted in Neon PostgreSQL. The system exposes task operations (add, list, complete, update, delete) as MCP tools that the AI agent can use to manage user tasks through natural language. Sequential integer IDs are used for all tasks and conversations to ensure consistent referencing. The frontend integrates OpenAI ChatKit into the existing dashboard UI while maintaining security through the existing authentication system.

## Technical Context

**Language/Version**: Python 3.13+, TypeScript 5.5+
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, Next.js 16+, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <200ms p95 response time for chat interactions, support 1000+ concurrent users
**Constraints**: Must be stateless server architecture, all state persisted in DB, sequential integer IDs for tasks/conversations
**Scale/Scope**: Individual user conversations, multi-tenant with user isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification:
- ✅ **Statelessness**: Server must be stateless with all state persisted in database (FR-009)
- ✅ **Sequential Integer IDs**: Tasks and conversations must use sequential integer IDs (FR-002)
- ✅ **Security**: AI chatbot must be protected by existing auth system (FR-006)
- ✅ **MCP Integration**: Task operations must be exposed through MCP tools (FR-008)
- ✅ **No Breaking Changes**: Existing Phase 2 Auth/Task logic must remain intact
- ✅ **OpenAI Agents SDK**: Must use OpenAI Agents SDK as mandated
- ✅ **Database Extensions**: Need Conversation and Message models in existing SQLModel
- ✅ **Frontend Integration**: Must integrate OpenAI ChatKit with existing dashboard theme

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

backend/
├── src/
│   ├── models.py            # Extended with Conversation and Message models
│   ├── mcp/
│   │   └── server.py        # MCP tools implementation for task operations
│   ├── agent/
│   │   └── runner.py        # OpenAI Agent logic and conversation handling
│   ├── routers/
│   │   ├── chat.py          # Chat API endpoint
│   │   └── tasks.py         # Existing task operations (unchanged)
│   ├── database.py          # Database connection and session management
│   └── main.py              # FastAPI app with MCP integration
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/
│   │   └── dashboard/
│   │       └── page.tsx     # Main dashboard with integrated chat
│   ├── components/
│   │   └── chat/
│   │       └── ChatInterface.tsx  # OpenAI ChatKit integration
│   └── services/
│       └── api.ts           # API client for chat endpoint
└── tests/

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | None       | All requirements compliant          |
