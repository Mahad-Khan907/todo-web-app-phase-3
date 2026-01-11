---
id: 1002
title: Constitution Update Phase III
stage: constitution
date: 2026-01-06
surface: project
model: Claude Sonnet 4.5
feature: none
branch: main
user: Mahad Khan
command: /sp.constitution
labels: [constitution, phase-iii, ai-chatbot, mcp, openai-agents]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - path: .specify/memory/constitution.md
    action: updated
    description: Updated constitution with Phase III requirements
tests:
  - path:
    action:
    description:
---

## Prompt

# Claude CLI Todo Web App Constitution - Phase III: AI Chatbot

## Project Overview
### Project Mission
To evolve the Phase 2 Todo Web App into an AI-native application. Phase III integrates a conversational AI interface using MCP (Model Context Protocol) and OpenAI Agents SDK to allow natural language task management.

## Technical Stack (Integrated)
- **Backend**: FastAPI, SQLModel, Neon DB, OpenAI Agents SDK, MCP SDK.
- **Frontend**: Next.js 16+, Tailwind CSS (Premium Dark Theme), OpenAI ChatKit.
- **Infrastructure**: Python 3.13 (uv), PostgreSQL (Neon Serverless).

## 🤖 Agent & Skill Mandate (CRITICAL)
Every operation performed during Phase III MUST utilize the specialized **Agents** and **Skills** located inside the `.claude/` folder.
- Direct execution by the primary model is prohibited for domain-specific tasks.
- **Skills** from `.claude/` must be used for database migrations, UI styling, and API logic to ensure "No Error" code delivery.

## Phase III Specific Rules
### 1. Unified State Management
- All AI operations must be **stateless** at the server level.
- Every chat request must trigger an **Agent** to:
  1. Fetch conversation history from the `Message` and `Conversation` tables.
  2. Execute MCP tools against the existing `Task` table.
  3. Store the response before returning to the client.

### 2. UI/UX Consistency
- The ChatKit interface must be injected into the existing Phase 2 Dashboard.
- **Styling Rule**: All new components must match the "Premium Dark Blue / Glassmorphism" theme of Phase 2 using the styling skills in `.claude/`.

### 3. Authentication & Security
- The AI endpoint (`/api/chat`) must be protected by the same JWT/Better Auth logic established in Phase 2.
- User ID isolation is mandatory: Users can only chat about and modify their own tasks.

## 📁 Project Structure (Phase III)
- `/specs/ai/`: All specification files for Phase III.
- `/backend/src/mcp/`: MCP Server and tool definitions.
- `/backend/src/agents/`: OpenAI Agent logic and runners.
- `/frontend/src/components/

## Response snapshot

I have successfully updated the project constitution to incorporate the Phase III AI Chatbot requirements. The constitution now includes:

- Updated project mission for Phase III AI-native application
- Enhanced technical stack with AI integration components
- Critical "🤖 Agent & Skill Mandate" requiring use of specialized agents
- Phase III specific rules for state management, UI consistency, and security
- Updated project structure for AI-specific directories
- Enhanced operational rules for AI integration

Version updated from 1.1.0 to 1.2.0 with comprehensive changes to support MCP tools, OpenAI Agents SDK, and ChatKit integration while maintaining the "No Error" policy.

## Outcome

- ✅ Impact: High - Constitution updated to support Phase III AI Chatbot requirements
- 🧪 Tests: N/A - Documentation update
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Implementation of MCP tools and AI agents as per new constitution
- 🧠 Reflection: Constitution now properly reflects AI-native application requirements with proper governance for agent-based development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly updated with all Phase III requirements
- Prompt variant (if applicable):
- Next experiment (smallest change to try): Begin implementing MCP tools as mandated by the new constitution
