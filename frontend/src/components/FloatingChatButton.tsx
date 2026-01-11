"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { MessageCircle, X } from 'lucide-react';
import ChatInterface from './chat/ChatInterface';
import { useQueryClient } from '@tanstack/react-query';

interface FloatingChatButtonProps {
  user?: any; 
}

export default function FloatingChatButton({ user }: FloatingChatButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [hasMounted, setHasMounted] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    setHasMounted(true);
  }, []);

  if (!hasMounted || !user) {
    return null;
  }

  return (
    <>
      {!isOpen && (
        <motion.button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white rounded-full p-4 shadow-lg shadow-blue-500/30"
          aria-label="Open chat"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          <MessageCircle className="h-6 w-6" />
        </motion.button>
      )}

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-6 inset-x-4 z-50 w-auto max-w-4xl h-[75vh] min-h-[500px] max-h-[80vh] bg-black/80 backdrop-blur-xl rounded-2xl border border-blue-500/30 shadow-2xl shadow-blue-500/20 overflow-hidden flex flex-col lg:w-1/2 lg:left-auto lg:right-6 xl:w-2/5"
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
          >
            <div className="flex-1 overflow-hidden flex flex-col">
              {/* CONNECTED THE ONCLOSE PROP HERE */}
              <ChatInterface 
                onClose={() => setIsOpen(false)} 
                onTaskChange={() => queryClient.invalidateQueries({ queryKey: ['tasks'] })} 
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}