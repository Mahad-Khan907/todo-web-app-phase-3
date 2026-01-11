---
id: 1002
title: Constitution Update Phase 3 AI Chatbot
stage: constitution
date: 2026-01-06
surface: project
model: Claude Sonnet 4.5
feature: none
branch: main
user: Mahad Khan
command: /sp.constitution
labels: [constitution, phase-3, ai-chatbot, mcp, openai-agents, spec-driven]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - path: .specify/memory/constitution.md
    action: updated
    description: Updated constitution with Phase 3 AI Chatbot requirements
tests:
  - path:
    action:
    description:
---

## Prompt

# Project Constitution: Todo AI Chatbot (Phase 3)

## Project Overview
This project is an evolution of a Todo Web App. Phase 2 (Infrastructure & Auth) is COMPLETE. Phase 3 focuses on building a Stateless AI Chatbot using MCP (Model Context Protocol) and OpenAI Agents SDK, integrated into the existing monorepo.

## Technical Stack (Phase 3 Integration)
- **Framework**: FastAPI (Backend), Next.js 16+ (Frontend)
- **AI Logic**: OpenAI Agents SDK + Official MCP SDK
- **MCP Server**: Integrated into FastAPI to expose Task operations as tools
- **Database**: Neon Serverless PostgreSQL (SQLModel ORM)
- **Auth**: Better Auth (Frontend) + JWT (Backend) - AI must be protected by existing auth
- **UI**: OpenAI ChatKit integrated into the existing Dashboard theme

## Phase 3 Core Rules
1. **Directory Structure**:
   - New specifications must be stored in `specs/003-ai-chatbot/`.
   - Backend logic stays in `backend/src/` (new modules: `mcp_server.py`, `agent_logic.py`).
   - Frontend chat interface must match the existing Dashboard's theme/styling.
2. **Statelessness**: The `/api/chat` endpoint and MCP tools MUST be stateless. All state (conversations/messages) must be persisted in the database.
3. **Sub-Agent Usage**: Claude Code (the sub-agent) MUST be used for all file modifications and terminal commands.
4. **No Breaking Changes**: Do not modify existing Phase 2 Auth or Task CRUD logic unless necessary for MCP tool integration. Reuse existing SQLModel models where possible.
5. **Security**: The AI Chatbot is only accessible to logged-in users. The `user_id` must be extracted from the existing auth dependency.

## Database Extensions
Phase 3 requires new models in `backend/src/models.py`:
- `Conversation`: `id`, `user_id`, `created_at`, `updated_at`
- `Message`: `id`, `conversation_id`, `user_id`, `role` (user/assistant), `content`, `created_at`

## Implementation Workflow (Spec-Driven)
1. **Specify**: Create `/specs/003-ai-chatbot/spec.md` for AI behavior and MCP tools.
2. **Plan**: Generate `/specs/003-ai-chatbot/plan.md` for implementation roadmap.

## Response snapshot

Constitution successfully updated with Phase 3 AI Chatbot requirements. Key changes include:
- Updated project mission to reflect Phase 2 completion and Phase 3 AI focus
- Enhanced technical stack with MCP SDK and OpenAI Agents SDK
- Added Phase 3 Core Rules covering directory structure, statelessness, sub-agent usage, no breaking changes, and security
- Added Database Extensions section with required models
- Added Implementation Workflow section
- Version incremented from 1.2.0 to 1.3.0

## Outcome

- ✅ Impact: High - Constitution updated with comprehensive Phase 3 AI Chatbot requirements
- 🧪 Tests: N/A - Documentation update
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Implementation of MCP tools and AI agents as per new constitution
- 🧠 Reflection: Constitution now properly aligned with Phase 3 objectives for AI-native todo application

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly updated with all Phase 3 requirements
- Prompt variant (if applicable):
- Next experiment (smallest change to try): Begin implementing MCP tools as mandated by the new constitution
