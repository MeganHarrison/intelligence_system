'use client'

import { useEffect, useRef, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  MessageSquare, 
  Plus, 
  MoreHorizontal, 
  Trash2, 
  Download,
  RefreshCw,
  Settings
} from 'lucide-react'
import MessageBubble from './message-bubble'
import ChatInput from './chat-input'
import { 
  useChatStore,
  useCurrentSession,
  useCurrentMessages,
  useChatUI,
  useChatSuggestions,
  ChatMessage,
  ChatSuggestion
} from '@/lib/stores/chat'
import { ApiService } from '@/lib/utils/api'
import { useConnectionStatus } from '@/lib/providers/dashboard-provider'
import { toast } from 'sonner'

interface ChatInterfaceProps {
  className?: string
}

export function ChatInterface({ className }: ChatInterfaceProps) {
  const currentSession = useCurrentSession()
  const messages = useCurrentMessages()
  const { isLoading, isTyping, error } = useChatUI()
  const suggestions = useChatSuggestions()
  const { isApiConnected } = useConnectionStatus()
  
  const {
    createSession,
    addMessage,
    updateMessage,
    deleteMessage,
    clearSession,
    setLoading,
    setTyping,
    setError
  } = useChatStore()

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [retryingMessageId, setRetryingMessageId] = useState<string | null>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Create initial session if none exists
  useEffect(() => {
    if (!currentSession && !isLoading) {
      createSession()
    }
  }, [currentSession, createSession, isLoading])

  const handleSendMessage = async (content: string, files?: File[]) => {
    if (!currentSession || !isApiConnected) {
      toast.error('Please check your connection')
      return
    }

    if (!content.trim()) return

    // Add user message
    addMessage(currentSession.id, {
      content,
      role: 'user',
      metadata: {
        type: 'question'
      }
    })

    // Add loading message for AI response
    const loadingMessageId = `loading_${Date.now()}`
    addMessage(currentSession.id, {
      content: '',
      role: 'assistant',
      isLoading: true,
      metadata: {
        type: 'strategic'
      }
    })

    try {
      setLoading(true)
      setTyping(true)
      setError(null)

      // Send message to API
      const response = await ApiService.sendChatMessage({
        message: content,
        context: {
          sessionId: currentSession.id,
          previousMessages: messages.slice(-5).map(m => ({
            role: m.role,
            content: m.content
          }))
        }
      })

      // Remove loading message and add real response
      deleteMessage(currentSession.id, loadingMessageId)
      addMessage(currentSession.id, {
        content: response.response,
        role: 'assistant',
        metadata: {
          type: 'strategic',
          confidence: 85, // Could be from API response
          sources: ['Strategic Intelligence Database', 'Market Analysis Engine']
        }
      })

      toast.success('Response received')
    } catch (error) {
      console.error('Chat error:', error)
      
      // Remove loading message and add error message
      deleteMessage(currentSession.id, loadingMessageId)
      addMessage(currentSession.id, {
        content: "I apologize, but I'm having trouble processing your request right now. Please check the connection and try again.",
        role: 'assistant',
        metadata: {
          type: 'strategic',
          confidence: 0
        }
      })

      setError('Failed to send message')
      toast.error('Failed to get response')
    } finally {
      setLoading(false)
      setTyping(false)
    }
  }

  const handleSuggestionSelect = (suggestion: ChatSuggestion) => {
    handleSendMessage(suggestion.text)
  }

  const handleRetryMessage = async (messageId: string) => {
    if (!currentSession) return

    const message = messages.find(m => m.id === messageId)
    if (!message) return

    // Find the user message that triggered this response
    const messageIndex = messages.findIndex(m => m.id === messageId)
    const previousUserMessage = messages
      .slice(0, messageIndex)
      .reverse()
      .find(m => m.role === 'user')

    if (previousUserMessage) {
      setRetryingMessageId(messageId)
      
      // Update message to show loading state
      updateMessage(currentSession.id, messageId, {
        content: '',
        isLoading: true
      })

      try {
        setLoading(true)
        setTyping(true)

        const response = await ApiService.sendChatMessage({
          message: previousUserMessage.content,
          context: {
            sessionId: currentSession.id,
            isRetry: true
          }
        })

        // Update with new response
        updateMessage(currentSession.id, messageId, {
          content: response.response,
          isLoading: false,
          metadata: {
            type: 'strategic',
            confidence: 85,
            sources: ['Strategic Intelligence Database']
          }
        })

        toast.success('Message retried successfully')
      } catch (error) {
        console.error('Retry error:', error)
        
        updateMessage(currentSession.id, messageId, {
          content: "I'm still having trouble with this request. Please try rephrasing your question.",
          isLoading: false,
          metadata: {
            type: 'strategic',
            confidence: 0
          }
        })

        toast.error('Retry failed')
      } finally {
        setLoading(false)
        setTyping(false)
        setRetryingMessageId(null)
      }
    }
  }

  const handleDeleteMessage = (messageId: string) => {
    if (!currentSession) return
    deleteMessage(currentSession.id, messageId)
    toast.success('Message deleted')
  }

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content)
    toast.success('Message copied to clipboard')
  }

  const handleNewChat = () => {
    createSession()
    toast.success('New chat started')
  }

  const handleClearChat = () => {
    if (!currentSession) return
    clearSession(currentSession.id)
    toast.success('Chat cleared')
  }

  const handleExportChat = () => {
    if (!currentSession || messages.length === 0) return

    const chatContent = messages
      .map(msg => `${msg.role.toUpperCase()}: ${msg.content}`)
      .join('\n\n')

    const blob = new Blob([chatContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `chat-${currentSession.title}-${new Date().toISOString().split('T')[0]}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    toast.success('Chat exported')
  }

  if (!currentSession) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <MessageSquare className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-muted-foreground">Loading chat...</p>
        </div>
      </div>
    )
  }

  return (
    <Card className={`h-full flex flex-col ${className}`}>
      {/* Chat Header */}
      <CardHeader className="flex-shrink-0 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <MessageSquare className="h-5 w-5" />
            <div>
              <CardTitle className="text-lg">{currentSession.title}</CardTitle>
              <p className="text-sm text-muted-foreground">
                {messages.length} messages
                {!isApiConnected && ' • Offline'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Badge variant={isApiConnected ? "default" : "destructive"}>
              {isApiConnected ? 'Connected' : 'Offline'}
            </Badge>
            
            <Button variant="ghost" size="icon" onClick={handleNewChat}>
              <Plus className="h-4 w-4" />
            </Button>
            
            <Button variant="ghost" size="icon" onClick={handleExportChat}>
              <Download className="h-4 w-4" />
            </Button>
            
            <Button variant="ghost" size="icon" onClick={handleClearChat}>
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>

      {/* Messages Area */}
      <CardContent className="flex-1 p-0 overflow-hidden">
        <ScrollArea className="h-full px-4 py-4">
          <div className="space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-8">
                <MessageSquare className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">Start a conversation with your strategic AI assistant</p>
              </div>
            ) : (
              messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  message={message}
                  onDelete={handleDeleteMessage}
                  onRetry={handleRetryMessage}
                  onCopy={handleCopyMessage}
                />
              ))
            )}
            
            {/* Error Display */}
            {error && (
              <div className="text-center py-4">
                <p className="text-sm text-destructive">{error}</p>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => setError(null)}
                  className="mt-2"
                >
                  Dismiss
                </Button>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>
      </CardContent>

      {/* Chat Input */}
      <div className="flex-shrink-0 border-t p-4">
        <ChatInput
          onSendMessage={handleSendMessage}
          onSuggestionSelect={handleSuggestionSelect}
          suggestions={suggestions}
          isLoading={isLoading}
          isTyping={isTyping}
          allowFiles={false} // Can be enabled later
          allowVoice={false} // Can be enabled later
        />
      </div>
    </Card>
  )
}

export default ChatInterface