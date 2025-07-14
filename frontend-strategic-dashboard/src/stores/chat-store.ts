"use client";

import { create } from 'zustand';
import axios from 'axios';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  error?: boolean;
}

interface ChatState {
  messages: Message[];
  isConnected: boolean;
  socket: WebSocket | null;
  isLoading: boolean;
  isInitialized: boolean;
  
  // Actions
  addMessage: (message: Message) => void;
  sendMessage: (content: string) => Promise<void>;
  connect: () => void;
  disconnect: () => void;
  clearMessages: () => void;
  initialize: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isConnected: false,
  socket: null,
  isLoading: false,
  isInitialized: false,

  addMessage: (message: Message) => {
    set((state) => ({
      messages: [...state.messages, message]
    }));
  },

  sendMessage: async (content: string) => {
    const state = get();
    
    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: new Date()
    };
    
    state.addMessage(userMessage);
    set({ isLoading: true });

    try {
      // Send to backend API
      const response = await axios.post('http://localhost:8000/api/chat/message', {
        message: content,
        context: null,
        client_id: 'dashboard-client'
      });

      // Add AI response
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.response,
        isUser: false,
        timestamp: new Date()
      };
      
      state.addMessage(aiMessage);
      
    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm having trouble connecting to the strategic intelligence system. Please check that the backend is running and try again.",
        isUser: false,
        timestamp: new Date(),
        error: true
      };
      
      state.addMessage(errorMessage);
    } finally {
      set({ isLoading: false });
    }
  },

  connect: () => {
    const state = get();
    if (state.socket || typeof window === 'undefined') return;

    try {
      // Create WebSocket connection for real-time updates
      const clientId = 'dashboard-client';
      const wsUrl = `ws://localhost:8000/ws/${clientId}`;
      
      console.log('Attempting to connect to WebSocket:', wsUrl);
      const newSocket = new WebSocket(wsUrl);

      newSocket.onopen = () => {
        console.log('Connected to strategic intelligence system');
        set({ isConnected: true });
      };

      newSocket.onclose = () => {
        console.log('Disconnected from strategic intelligence system');
        set({ isConnected: false, socket: null });
      };

      newSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        set({ isConnected: false });
      };

      newSocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'strategic_update') {
            const updateMessage: Message = {
              id: Date.now().toString(),
              content: `📊 Strategic Update: ${data.message}`,
              isUser: false,
              timestamp: new Date()
            };
            get().addMessage(updateMessage);
          } else if (data.type === 'workflow_complete') {
            const workflowMessage: Message = {
              id: Date.now().toString(),
              content: `✅ Workflow Complete: ${data.workflow_id}\n\nResults: ${JSON.stringify(data.results, null, 2)}`,
              isUser: false,
              timestamp: new Date()
            };
            get().addMessage(workflowMessage);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      set({ socket: newSocket });
      
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      set({ isConnected: false });
    }
  },

  disconnect: () => {
    const state = get();
    if (state.socket) {
      state.socket.close();
      set({ socket: null, isConnected: false });
    }
  },

  clearMessages: () => {
    set({ messages: [] });
  },

  initialize: () => {
    const state = get();
    if (state.isInitialized || typeof window === 'undefined') return;

    // Add initial welcome message
    const welcomeMessage: Message = {
      id: 'welcome',
      content: "🤖 AI Chief of Staff Ready\n\nI'm connected via HTTP API and ready to help with strategic analysis. WebSocket connection will be attempted in the background for real-time updates.",
      isUser: false,
      timestamp: new Date()
    };
    
    state.addMessage(welcomeMessage);
    state.connect();
    set({ isInitialized: true });
  }
}));