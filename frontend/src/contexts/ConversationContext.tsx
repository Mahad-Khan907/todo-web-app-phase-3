"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface Message {
  id: number | string;
  role: 'user' | 'assistant';
  content: string;
}

interface ConversationContextType {
  selectedConversation: number | null;
  setSelectedConversation: (id: number | null) => void;
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  conversations: any[];
  setConversations: React.Dispatch<React.SetStateAction<any[]>>;
  resetToNewChat: () => void; // Added for convenience
}

const ConversationContext = createContext<ConversationContextType | undefined>(undefined);

export function ConversationProvider({ children }: { children: ReactNode }) {
  const [selectedConversation, setSelectedConversation] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<any[]>([]);

  // 1. Persist the selected chat on refresh
  useEffect(() => {
    const saved = localStorage.getItem('selectedConversation');
    // Check if saved value is valid and not "null" or "undefined"
    if (saved && saved !== "null" && saved !== "undefined") {
      const parsedId = parseInt(saved, 10);
      if (!isNaN(parsedId)) {
        setSelectedConversation(parsedId);
      }
    }
  }, []);

  // 2. Update localStorage when selection changes
  useEffect(() => {
    if (selectedConversation === null) {
      localStorage.removeItem('selectedConversation');
    } else {
      localStorage.setItem('selectedConversation', selectedConversation.toString());
    }
  }, [selectedConversation]);

  // 3. Helper to force a new chat state
  const resetToNewChat = () => {
    setSelectedConversation(null);
    setMessages([]);
    localStorage.removeItem('selectedConversation');
  };

  return (
    <ConversationContext.Provider value={{
      selectedConversation, setSelectedConversation,
      messages, setMessages,
      conversations, setConversations,
      resetToNewChat
    }}>
      {children}
    </ConversationContext.Provider>
  );
}

export function useConversation() {
  const context = useContext(ConversationContext);
  if (!context) throw new Error('useConversation must be used within Provider');
  return context;
}