"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useConversation } from "@/contexts/ConversationContext";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Bot, User, Plus, MessageSquare, History, Sparkles, Loader2, X, Menu, Trash2, ExternalLink } from "lucide-react";
import api from "@/lib/api";
import { cn } from "@/lib/utils";

export default function ChatInterface({ onTaskChange, onClose }: { onTaskChange?: () => void, onClose?: () => void }) {
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMessagesLoading, setIsMessagesLoading] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { user } = useAuth();

  const {
    messages, setMessages,
    selectedConversation, setSelectedConversation,
    conversations, setConversations,
    resetToNewChat
  } = useConversation() as any;

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTo({
          top: scrollContainer.scrollHeight,
          behavior: "smooth"
        });
      }
    }
  }, [messages, isLoading]);

  const fetchMessages = useCallback(async (id: number) => {
    setIsMessagesLoading(true);
    try {
      const res = await api.get(`/chat/conversations/${id}`);
      setMessages(res.data.messages.map((m: any) => ({
        id: m.id, role: m.role, content: m.content
      })));
    } catch (e) {
      console.error("Failed to load chat history");
      resetToNewChat();
    } finally {
      setIsMessagesLoading(false);
    }
  }, [setMessages, resetToNewChat]);

  const loadHistory = useCallback(async (shouldFetchMessages = false) => {
    if (!user) return;
    try {
      const res = await api.get("/chat/conversations");
      const history = res.data || [];
      setConversations(history);

      if (selectedConversation) {
        const exists = history.some((c: any) => c.id === selectedConversation);
        if (exists && shouldFetchMessages) {
          fetchMessages(selectedConversation);
        } else if (!exists) {
          resetToNewChat();
        }
      }
    } catch (e) {
        setConversations([]);
        console.error("History fetch failed");
    }
  }, [user, setConversations, selectedConversation, fetchMessages, resetToNewChat]);

  useEffect(() => {
    loadHistory(true);
  }, []);

  const handleSelectChat = async (id: number) => {
    if (selectedConversation === id) return;
    setSelectedConversation(id);
    setMessages([]);
    setIsMobileMenuOpen(false);
    await fetchMessages(id);
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    const msg = inputValue;
    const tempId = Date.now();
    setMessages((prev: any[]) => [...prev, { id: tempId, role: 'user', content: msg }]);
    setInputValue("");
    setIsLoading(true);

    try {
      const res = await api.post("/chat/", {
        message: msg,
        conversation_id: selectedConversation
      });

      setMessages((prev: any[]) => [...prev, {
        id: res.data.assistant_message_id,
        role: 'assistant',
        content: res.data.message
      }]);

      if (!selectedConversation) {
        setSelectedConversation(res.data.conversation_id);
        loadHistory(false);
      }
      if (onTaskChange) onTaskChange();
    } catch (error) {
      console.error("Chat Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteChat = async (e: React.MouseEvent, id: number, title: string) => {
    e.stopPropagation();
    if (window.confirm(`Are you sure you want to delete "${title || 'Untitled Thread'}"?`)) {
      try {
        await api.delete(`/chat/conversations/${id}`);
        setConversations((prev: any[]) => prev.filter(c => c.id !== id));
        if (selectedConversation === id) resetToNewChat();
      } catch (error) {
        console.error("Failed to delete conversation:", error);
      }
    }
  };

  const SidebarContent = () => (
    <>
      <div className="p-4 border-b border-white/[0.05] flex justify-between items-center">
        <Button
          onClick={() => { resetToNewChat(); setIsMobileMenuOpen(false); }}
          className="flex-1 bg-zinc-100 hover:bg-white text-black font-semibold text-xs h-9 rounded-lg transition-all active:scale-95"
        >
          <Plus className="h-3.5 w-3.5 mr-2" /> New Chat
        </Button>
        <button onClick={() => setIsMobileMenuOpen(false)} className="md:hidden ml-2 p-1 text-zinc-500">
          <X className="h-4 w-4" />
        </button>
      </div>

      <ScrollArea className="flex-1 px-2 py-3">
        <div className="flex items-center gap-2 px-3 mb-3 text-zinc-500">
          <History className="h-3 w-3" />
          <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-600">Recent Activity</span>
        </div>
        <div className="space-y-0.5">
          {conversations.length === 0 ? (
            <p className="text-[11px] text-zinc-600 px-3 py-4 italic">No chat history yet</p>
          ) : (
            conversations.map((c: { id: number; title: string }) => (
              <div
                key={c.id}
                className={cn(
                  "group relative w-full flex items-center gap-1 px-2 py-1 rounded-md transition-all",
                  selectedConversation === c.id ? "bg-blue-600/10 border border-blue-500/20" : "hover:bg-white/[0.03]"
                )}
              >
                {/* 1. DELETE BUTTON (LEFT SIDE) */}
                <button
                  onClick={(e) => handleDeleteChat(e, c.id, c.title)}
                  className="p-1 rounded-md text-zinc-400 hover:text-red-400 hover:bg-red-500/10 opacity-100 transition-all"
                  title="Delete chat"
                >
                  <X className="h-3 w-3" />
                </button>

                {/* 2. OPEN CHAT BUTTON */}
                <button
                  onClick={() => handleSelectChat(c.id)}
                  className={cn(
                    "flex-1 flex items-center gap-2.5 py-1.5 overflow-hidden text-left transition-colors",
                    selectedConversation === c.id ? "text-blue-400" : "text-zinc-500 group-hover:text-zinc-200"
                  )}
                >
                  <MessageSquare className={cn("h-3.5 w-3.5 shrink-0", selectedConversation === c.id ? "text-blue-400" : "text-zinc-600")} />
                  <span className="truncate text-[12px]">{c.title || "Untitled Thread"}</span>
                </button>
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </>
  );

  return (
    <div className="flex h-full w-full bg-[#09090b] text-zinc-300 font-sans selection:bg-blue-500/30 overflow-hidden relative">
      {isMobileMenuOpen && (
        <div className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)} />
      )}

      <aside className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-[#0c0c0e] border-r border-white/[0.05] transition-transform duration-300 md:relative md:translate-x-0 md:flex md:flex-col md:w-56 shrink-0",
        isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <SidebarContent />
      </aside>

      <main className="flex-1 flex flex-col bg-[#09090b] relative w-full">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,_rgba(59,130,246,0.05),transparent_50%)] pointer-events-none" />

        <header className="h-14 flex items-center justify-between px-4 md:px-6 border-b border-white/[0.05] z-10 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <button onClick={() => setIsMobileMenuOpen(true)} className="md:hidden p-1.5 hover:bg-white/10 rounded-md text-zinc-400">
              <Menu className="h-5 w-5" />
            </button>
            <div className="flex items-center">
              <Sparkles className="h-4 w-4 text-blue-500 mr-2" />
              <h2 className="text-[10px] md:text-xs font-semibold tracking-widest uppercase text-zinc-400 truncate">Todo Manager AI</h2>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 hover:bg-white/10 rounded-md transition-colors text-zinc-500 hover:text-zinc-200">
            <X className="h-4 w-4" />
          </button>
        </header>

        <ScrollArea ref={scrollRef} className="flex-1 p-4 md:p-6 relative z-10">
          <div className="max-w-3xl mx-auto space-y-8">
            {isMessagesLoading ? (
              <div className="h-[60vh] flex flex-col items-center justify-center space-y-4">
                <Loader2 className="h-8 w-8 text-blue-500 animate-spin opacity-50" />
                <p className="text-xs font-medium text-zinc-600 uppercase tracking-tighter">Retrieving Encrypted History...</p>
              </div>
            ) : messages.length === 0 ? (
              <div className="h-[40vh] flex flex-col items-center justify-center text-center animate-in fade-in zoom-in duration-500">
                <div className="w-12 h-12 rounded-2xl bg-blue-600/10 flex items-center justify-center mb-4">
                  <Bot className="text-blue-500 w-6 h-6" />
                </div>
                <h1 className="text-lg md:text-xl font-medium text-white mb-2">How can I assist you today?</h1>
                <p className="text-zinc-500 text-xs md:text-sm max-w-xs">Manage tasks, update records, or brainstorm ideas with the AI Agent.</p>
              </div>
            ) : (
              messages.map((m: { id: number | string; role: 'user' | 'assistant'; content: string }, i: number) => (
                <div key={i} className={cn("flex gap-3 md:gap-4 group animate-in slide-in-from-bottom-2", m.role === 'user' ? "flex-row-reverse" : "flex-row")}>
                  <div className={cn(
                    "h-7 w-7 md:h-8 md:w-8 rounded-lg flex items-center justify-center shrink-0 shadow-sm border",
                    m.role === 'assistant' ? "bg-blue-600/10 border-blue-500/20 text-blue-400" : "bg-zinc-800 border-zinc-700 text-zinc-400"
                  )}>
                    {m.role === 'assistant' ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                  </div>
                  <div className={cn(
                    "px-3 py-2 md:px-4 md:py-3 rounded-2xl text-[13px] md:text-[14.5px] leading-relaxed shadow-sm max-w-[90%] md:max-w-[85%] transition-all",
                    m.role === 'user' ? "bg-blue-600 text-white shadow-blue-900/20" : "bg-[#121214] border border-white/[0.06] text-zinc-200"
                  )}>
                    {m.content}
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="flex gap-4 animate-pulse">
                <div className="h-8 w-8 rounded-lg bg-zinc-800" />
                <div className="space-y-2 flex-1">
                  <div className="h-3 bg-zinc-800 rounded w-1/4" />
                  <div className="h-3 bg-zinc-800 rounded w-3/4" />
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        <div className="p-4 md:p-6 bg-gradient-to-t from-[#09090b] via-[#09090b] to-transparent">
          <div className="max-w-3xl mx-auto relative">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
              placeholder="Type your message here..."
              className="w-full bg-[#121214] border border-white/[0.08] rounded-2xl p-3 md:p-4 pr-12 md:pr-14 text-[14px] md:text-[15px] resize-none focus:outline-none focus:ring-1 focus:ring-blue-500/50 shadow-2xl transition-all min-h-[50px] md:min-h-[56px]"
              rows={1}
            />
            <button
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
              className="absolute right-2 bottom-2 md:right-3 md:bottom-3 p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl transition-all disabled:opacity-30 active:scale-90"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
          <p className="text-[10px] text-center mt-3 text-zinc-600 uppercase tracking-widest">Powered by Model Context Protocol</p>
        </div>
      </main>
    </div>
  );
}