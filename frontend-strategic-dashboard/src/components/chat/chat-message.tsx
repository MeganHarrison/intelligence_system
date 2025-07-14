interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  error?: boolean;
}

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[70%] ${message.isUser ? 'order-2' : 'order-1'}`}>
        <div
          className={`rounded-lg px-4 py-2 ${
            message.isUser
              ? 'bg-blue-600 text-white'
              : message.error
              ? 'bg-red-50 text-red-800 border border-red-200'
              : 'bg-white text-gray-900 border border-gray-200'
          }`}
        >
          <div className="flex items-start space-x-2">
            {!message.isUser && (
              <div className="flex-shrink-0 mt-1">
                <div className="text-lg">
                  {message.error ? '⚠️' : '🤖'}
                </div>
              </div>
            )}
            <div className="flex-1">
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        </div>
        <div className={`text-xs text-gray-500 mt-1 ${message.isUser ? 'text-right' : 'text-left'}`}>
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
}