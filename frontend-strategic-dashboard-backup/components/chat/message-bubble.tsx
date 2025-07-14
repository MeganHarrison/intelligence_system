'use client'

import { memo } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Brain, 
  User, 
  Clock, 
  CheckCircle, 
  Copy, 
  MoreVertical,
  Trash2,
  RefreshCw
} from 'lucide-react'
import { ChatMessage } from '@/lib/stores/chat'
import { formatDistanceToNow } from 'date-fns'

interface MessageBubbleProps {
  message: ChatMessage
  onDelete?: (messageId: string) => void
  onRetry?: (messageId: string) => void
  onCopy?: (content: string) => void
}

export const MessageBubble = memo(function MessageBubble({ 
  message, 
  onDelete, 
  onRetry, 
  onCopy 
}: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'
  
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
    onCopy?.(message.content)
  }

  const getMessageIcon = () => {
    if (isUser) return <User className="h-4 w-4" />
    if (isSystem) return <CheckCircle className="h-4 w-4" />
    return <Brain className="h-4 w-4" />
  }

  const getMessageTypeColor = () => {
    switch (message.metadata?.type) {
      case 'strategic': return 'bg-blue-50 border-blue-200 text-blue-800'
      case 'analysis': return 'bg-green-50 border-green-200 text-green-800'
      case 'briefing': return 'bg-purple-50 border-purple-200 text-purple-800'
      case 'question': return 'bg-orange-50 border-orange-200 text-orange-800'
      default: return 'bg-gray-50 border-gray-200 text-gray-800'
    }
  }

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start space-x-3`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-primary text-primary-foreground' 
              : isSystem
                ? 'bg-orange-500 text-white'
                : 'bg-blue-500 text-white'
          }`}>
            {getMessageIcon()}
          </div>
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-1 flex-1`}>
          {/* Message Card */}
          <Card className={`${
            isUser 
              ? 'bg-primary text-primary-foreground' 
              : 'bg-background border-border'
          } shadow-sm`}>
            <CardContent className="px-4 py-3">
              {/* Message Type Badge */}
              {!isUser && message.metadata?.type && (
                <Badge 
                  variant="outline" 
                  className={`text-xs mb-2 ${getMessageTypeColor()}`}
                >
                  {message.metadata.type}
                </Badge>
              )}

              {/* Message Text */}
              <div className="prose prose-sm max-w-none">
                {message.isLoading ? (
                  <div className="flex items-center space-x-2">
                    <RefreshCw className="h-4 w-4 animate-spin" />
                    <span className="text-sm">Thinking...</span>
                  </div>
                ) : (
                  <p className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                  </p>
                )}
              </div>

              {/* Confidence Score */}
              {!isUser && message.metadata?.confidence && (
                <div className="mt-2 text-xs text-muted-foreground">
                  Confidence: {message.metadata.confidence}%
                </div>
              )}

              {/* Sources */}
              {!isUser && message.metadata?.sources && message.metadata.sources.length > 0 && (
                <div className="mt-2">
                  <div className="text-xs text-muted-foreground mb-1">Sources:</div>
                  <div className="flex flex-wrap gap-1">
                    {message.metadata.sources.slice(0, 3).map((source, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {source}
                      </Badge>
                    ))}
                    {message.metadata.sources.length > 3 && (
                      <Badge variant="secondary" className="text-xs">
                        +{message.metadata.sources.length - 3} more
                      </Badge>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Message Actions */}
          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
            <span className="flex items-center space-x-1">
              <Clock className="h-3 w-3" />
              <span>
                {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
              </span>
            </span>

            {/* Action Buttons */}
            <div className="flex items-center space-x-1">
              <Button
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0"
                onClick={handleCopy}
                title="Copy message"
              >
                <Copy className="h-3 w-3" />
              </Button>

              {!isUser && onRetry && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0"
                  onClick={() => onRetry(message.id)}
                  title="Retry message"
                >
                  <RefreshCw className="h-3 w-3" />
                </Button>
              )}

              {onDelete && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0 text-destructive hover:text-destructive"
                  onClick={() => onDelete(message.id)}
                  title="Delete message"
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
})

export default MessageBubble