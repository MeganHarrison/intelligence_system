'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  MessageSquare, 
  Plus, 
  Clock, 
  Brain,
  TrendingUp,
  Users,
  BarChart3
} from 'lucide-react'
import ChatInterface from '@/components/chat/chat-interface'
import { 
  useChatSessions, 
  useCurrentSession, 
  useChatStore 
} from '@/lib/stores/chat'
import { useConnectionStatus } from '@/lib/providers/dashboard-provider'

function ChatSidebar() {
  const sessions = useChatSessions()
  const currentSession = useCurrentSession()
  const { createSession, setCurrentSession } = useChatStore()
  const { isApiConnected } = useConnectionStatus()

  const handleNewChat = () => {
    const sessionId = createSession()
    setCurrentSession(sessionId)
  }

  const handleSelectSession = (sessionId: string) => {
    setCurrentSession(sessionId)
  }

  const recentSessions = sessions
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    .slice(0, 10)

  return (
    <Card className="h-full">
      <CardHeader className="border-b">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Chat Sessions</CardTitle>
          <Button 
            size="icon" 
            variant="outline"
            onClick={handleNewChat}
            disabled={!isApiConnected}
          >
            <Plus className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-sm text-muted-foreground">
          Strategic AI conversations
        </p>
      </CardHeader>
      
      <CardContent className="p-4">
        <div className="space-y-2">
          {recentSessions.length > 0 ? (
            recentSessions.map((session) => (
              <div
                key={session.id}
                className={`p-3 rounded-lg cursor-pointer transition-colors border ${
                  currentSession?.id === session.id
                    ? 'bg-primary/10 border-primary/20'
                    : 'hover:bg-muted border-transparent'
                }`}
                onClick={() => handleSelectSession(session.id)}
              >
                <div className="flex items-start justify-between space-x-2">
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium truncate">
                      {session.title}
                    </h4>
                    <p className="text-xs text-muted-foreground">
                      {session.messages.length} messages
                    </p>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Clock className="h-3 w-3 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">
                      {new Date(session.updatedAt).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                
                {/* Last message preview */}
                {session.messages.length > 0 && (
                  <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
                    {session.messages[session.messages.length - 1].content.substring(0, 100)}
                    {session.messages[session.messages.length - 1].content.length > 100 ? '...' : ''}
                  </p>
                )}
              </div>
            ))
          ) : (
            <div className="text-center py-8">
              <MessageSquare className="mx-auto h-8 w-8 text-muted-foreground mb-2" />
              <p className="text-sm text-muted-foreground">No chat sessions yet</p>
              <Button 
                variant="outline" 
                size="sm" 
                className="mt-2"
                onClick={handleNewChat}
                disabled={!isApiConnected}
              >
                Start your first chat
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

function ChatStats() {
  const sessions = useChatSessions()
  const { isApiConnected } = useConnectionStatus()

  const totalMessages = sessions.reduce((sum, session) => sum + session.messages.length, 0)
  const activeSessions = sessions.filter(s => s.isActive).length
  const avgMessagesPerSession = sessions.length > 0 ? Math.round(totalMessages / sessions.length) : 0

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Sessions</CardTitle>
          <MessageSquare className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{sessions.length}</div>
          <p className="text-xs text-muted-foreground">
            {activeSessions} active
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Messages</CardTitle>
          <BarChart3 className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totalMessages}</div>
          <p className="text-xs text-muted-foreground">
            Strategic conversations
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Avg per Session</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{avgMessagesPerSession}</div>
          <p className="text-xs text-muted-foreground">
            Messages per chat
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default function ChatPage() {
  const { isApiConnected } = useConnectionStatus()
  const [showSidebar, setShowSidebar] = useState(true)

  return (
    <div className="bg-background">
      {/* Main Content */}
      <div className="container py-6">
        <div className="space-y-6">
          {/* Page Header */}
          <div>
            <h1 className="text-3xl font-bold tracking-tight">AI Strategic Assistant</h1>
            <p className="text-muted-foreground">
              Get strategic insights, market analysis, and business intelligence through AI-powered conversations
            </p>
          </div>

          {/* Connection Warning */}
          {!isApiConnected && (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center space-x-2 text-destructive">
                  <Brain className="h-4 w-4" />
                  <span className="text-sm font-medium">
                    AI Assistant is offline. Please check your backend connection.
                  </span>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Chat Stats */}
          <ChatStats />

          {/* Chat Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[600px]">
            {/* Sidebar */}
            {showSidebar && (
              <div className="lg:col-span-1">
                <ChatSidebar />
              </div>
            )}
            
            {/* Main Chat */}
            <div className={showSidebar ? "lg:col-span-3" : "lg:col-span-4"}>
              <ChatInterface className="h-full" />
            </div>
          </div>

          {/* Usage Tips */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Usage Tips</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="h-4 w-4 text-blue-500" />
                    <span className="font-medium text-sm">Strategic Analysis</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Ask about market trends, competitive positioning, and strategic opportunities
                  </p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <BarChart3 className="h-4 w-4 text-green-500" />
                    <span className="font-medium text-sm">Data Analysis</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Request analysis of business metrics, performance indicators, and trends
                  </p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Users className="h-4 w-4 text-purple-500" />
                    <span className="font-medium text-sm">Competitive Intelligence</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Get insights on competitors, market dynamics, and industry analysis
                  </p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Brain className="h-4 w-4 text-orange-500" />
                    <span className="font-medium text-sm">Executive Briefings</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Generate summaries, reports, and strategic recommendations
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}