'use client'

import { useState, useRef, useCallback, KeyboardEvent } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  Send, 
  Paperclip, 
  Mic, 
  Square,
  Lightbulb
} from 'lucide-react'
import { ChatSuggestion } from '@/lib/stores/chat'

interface ChatInputProps {
  onSendMessage: (message: string, files?: File[]) => void
  onSuggestionSelect: (suggestion: ChatSuggestion) => void
  suggestions: ChatSuggestion[]
  isLoading?: boolean
  isTyping?: boolean
  placeholder?: string
  maxLength?: number
  allowFiles?: boolean
  allowVoice?: boolean
}

export function ChatInput({
  onSendMessage,
  onSuggestionSelect,
  suggestions,
  isLoading = false,
  isTyping = false,
  placeholder = "Ask about strategic priorities, market analysis, or competitive intelligence...",
  maxLength = 1000,
  allowFiles = false,
  allowVoice = false
}: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [isRecording, setIsRecording] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)
  const inputRef = useRef<HTMLInputElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSend = useCallback(() => {
    const trimmedMessage = message.trim()
    if (!trimmedMessage && selectedFiles.length === 0) return
    if (isLoading || isTyping) return

    onSendMessage(trimmedMessage, selectedFiles)
    setMessage('')
    setSelectedFiles([])
    setShowSuggestions(false)
    
    // Focus back to input
    setTimeout(() => {
      inputRef.current?.focus()
    }, 100)
  }, [message, selectedFiles, isLoading, isTyping, onSendMessage])

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestionClick = (suggestion: ChatSuggestion) => {
    onSuggestionSelect(suggestion)
    setMessage(suggestion.text)
    setShowSuggestions(false)
    setTimeout(() => {
      inputRef.current?.focus()
    }, 100)
  }

  const handleFileSelect = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setSelectedFiles(prev => [...prev, ...files])
  }

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleVoiceToggle = () => {
    setIsRecording(!isRecording)
    // Voice recording implementation would go here
  }

  const getSuggestionIcon = (category: string) => {
    switch (category) {
      case 'strategic': return '🎯'
      case 'analysis': return '📊'
      case 'operations': return '⚙️'
      case 'intelligence': return '🔍'
      default: return '💡'
    }
  }

  const canSend = message.trim().length > 0 || selectedFiles.length > 0

  return (
    <div className="space-y-4">
      {/* Suggestions */}
      {showSuggestions && suggestions.length > 0 && message.length === 0 && (
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Lightbulb className="h-4 w-4" />
            <span>Suggested questions:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {suggestions.slice(0, 4).map((suggestion) => (
              <Button
                key={suggestion.id}
                variant="outline"
                size="sm"
                className="text-xs h-8 justify-start"
                onClick={() => handleSuggestionClick(suggestion)}
                disabled={isLoading}
              >
                <span className="mr-1">{getSuggestionIcon(suggestion.category)}</span>
                {suggestion.text}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedFiles.map((file, index) => (
            <Badge 
              key={index} 
              variant="secondary" 
              className="text-xs py-1 px-2 cursor-pointer hover:bg-destructive hover:text-destructive-foreground"
              onClick={() => removeFile(index)}
            >
              <Paperclip className="h-3 w-3 mr-1" />
              {file.name}
              <span className="ml-1 text-xs opacity-60">×</span>
            </Badge>
          ))}
        </div>
      )}

      {/* Input Area */}
      <div className="flex items-end space-x-2">
        <div className="flex-1 relative">
          <Input
            ref={inputRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isLoading ? "Processing..." : isTyping ? "AI is typing..." : placeholder}
            disabled={isLoading || isTyping}
            maxLength={maxLength}
            className="pr-12"
            autoComplete="off"
          />
          
          {/* Character Count */}
          {message.length > maxLength * 0.8 && (
            <div className="absolute right-2 top-1/2 transform -translate-y-1/2 text-xs text-muted-foreground">
              {message.length}/{maxLength}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-1">
          {/* File Upload */}
          {allowFiles && (
            <>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={handleFileSelect}
                disabled={isLoading || isTyping}
                className="h-10 w-10"
              >
                <Paperclip className="h-4 w-4" />
              </Button>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                className="hidden"
                onChange={handleFileChange}
                accept=".pdf,.doc,.docx,.txt,.md"
              />
            </>
          )}

          {/* Voice Recording */}
          {allowVoice && (
            <Button
              type="button"
              variant={isRecording ? "destructive" : "ghost"}
              size="icon"
              onClick={handleVoiceToggle}
              disabled={isLoading || isTyping}
              className="h-10 w-10"
            >
              {isRecording ? <Square className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
            </Button>
          )}

          {/* Send Button */}
          <Button
            type="button"
            onClick={handleSend}
            disabled={!canSend || isLoading || isTyping}
            className="h-10 w-10"
            size="icon"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Status Indicators */}
      {(isLoading || isTyping) && (
        <div className="flex items-center space-x-2 text-sm text-muted-foreground">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
          <span>{isLoading ? 'Processing your request...' : 'AI is typing...'}</span>
        </div>
      )}
    </div>
  )
}

export default ChatInput