"use client";

import { useRef, useEffect } from 'react';
import { ChatMessage } from '@/components/chat/chat-message';
import { ChatInput } from '@/components/chat/chat-input';
import { useChatStore } from '@/stores/chat-store';
import { ErrorBoundary } from '@/components/error-boundary';

export default function ChatPage() {
  const { messages, isConnected, sendMessage, addMessage, initialize } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize the store on component mount
  useEffect(() => {
    initialize();
  }, [initialize]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    try {
      await sendMessage(content);
    } catch {
      addMessage({
        id: Date.now().toString(),
        content: "Sorry, I couldn't process your message. Please try again.",
        isUser: false,
        timestamp: new Date(),
        error: true
      });
    }
  };

  return (
    <ErrorBoundary>
      <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">AI Strategic Chat</h1>
            <p className="text-sm text-gray-600">Chat with your AI Chief of Staff</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
            <span className="text-sm text-gray-600">
              {isConnected ? 'WebSocket Connected' : 'HTTP API Mode'}
            </span>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🤖</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Welcome to Strategic Chat</h3>
            <p className="text-gray-600 max-w-md mx-auto">
              Start a conversation with your AI Chief of Staff. Ask about business insights, 
              strategic analysis, or request workflow execution.
            </p>
            <div className="mt-6 bg-blue-50 rounded-lg p-4 max-w-lg mx-auto">
              <p className="text-sm text-blue-800 font-medium mb-2">Try asking:</p>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• &quot;What are the latest insights from our projects?&quot;</li>
                <li>• &quot;Analyze our partnership with Alleato Group&quot;</li>
                <li>• &quot;Show me construction project updates&quot;</li>
              </ul>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <div className="border-t border-gray-200 bg-white px-6 py-4">
        <ChatInput 
          onSendMessage={handleSendMessage}
          disabled={false}
          placeholder="Ask your AI Chief of Staff..."
        />
      </div>
    </div>
    </ErrorBoundary>
  );
}