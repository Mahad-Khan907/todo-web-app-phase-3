---
name: ChatKit Integration
description: Reusable OpenAI ChatKit UI integration for natural language task management with state management and backend connectivity.
model: sonnet
---

Reusable Skill:

Skill: ChatKit UI Integration – Input: Backend API configuration, authentication context, and UI customization requirements; Output: Full ChatKit UI implementation with state management, real-time interactions, authentication handling, and responsive design.

Usage Example:
```tsx
// Realistic example of ChatKit UI integration
'use client';

import { useChat } from 'ai/react';
import { Chat, type ChatProps } from '@openai/chatkit-react';
import { useEffect, useState } from 'react';

interface TaskChatProps {
  userId: string;
  authToken: string;
}

export function TaskChat({ userId, authToken }: TaskChatProps) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    body: { userId },
    headers: { Authorization: `Bearer ${authToken}` }
  });

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto">
        {messages.map((message) => (
          <div key={message.id} className={`p-4 ${message.role === 'user' ? 'bg-blue-50' : 'bg-gray-50'}`}>
            {message.content}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="border-t p-4">
        <input
          value={input}
          placeholder="Ask to add, list, or manage tasks..."
          onChange={handleInputChange}
          className="w-full p-2 border rounded"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading} className="mt-2 p-2 bg-blue-500 text-white rounded">
          Send
        </button>
      </form>
    </div>
  );
}
```

Notes:

This integration provides a natural language interface for task management using OpenAI ChatKit. It handles authentication, real-time messaging, state management, and responsive design. The component integrates seamlessly with the existing dashboard UI and connects to the backend chat endpoint.