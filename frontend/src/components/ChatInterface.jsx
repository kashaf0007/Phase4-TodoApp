// frontend/src/components/ChatInterface.jsx
import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { sendChatMessage, createNewConversation } from '../services/apiService';
import { UI_LOADING_MESSAGE, UI_ERROR_MESSAGE } from '../utils/constants';
import { formatErrorMessage } from '../utils/errorHandler';

const ChatInterface = ({ userId, initialConversationId = null }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(initialConversationId);

  // Initialize conversation
  useEffect(() => {
    const initializeConversation = async () => {
      // Check if user is authenticated
      if (!userId) {
        setError('You must be logged in to use the chat feature.');
        return;
      }

      if (!initialConversationId) {
        try {
          const newConversation = await createNewConversation(userId);
          setConversationId(newConversation.conversation_id);

          // Add welcome message
          setMessages([{
            id: 'welcome',
            message: 'Hello! I\'m your AI assistant. How can I help you today?',
            sender: 'assistant',
            timestamp: new Date(),
          }]);
        } catch (err) {
          console.error('Error initializing conversation:', err);
          setError(formatErrorMessage(err));
        }
      } else {
        setConversationId(initialConversationId);
        // Add welcome message for existing conversation
        setMessages([{
          id: 'welcome',
          message: 'Welcome back! Continuing our conversation...',
          sender: 'assistant',
          timestamp: new Date(),
        }]);
      }
    };

    initializeConversation();
  }, [initialConversationId, userId]);

  const handleSend = async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now().toString(),
      message: messageText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Call the backend API to get the response
      const response = await sendChatMessage(userId, messageText, conversationId);

      // Update conversation ID if it was returned
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant's response to the chat
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        message: response.response || 'I\'m sorry, I didn\'t understand that.',
        sender: 'assistant',
        timestamp: new Date(),
        toolCalls: response.tool_calls || [],
        confirmation: response.confirmation || null,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(formatErrorMessage(err));

      // Add error message to the chat
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        message: UI_ERROR_MESSAGE,
        sender: 'assistant',
        timestamp: new Date(),
        isError: true,
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to start a new conversation
  const startNewConversation = async () => {
    try {
      const newConversation = await createNewConversation(userId);
      setConversationId(newConversation.conversation_id);
      setMessages([{
        id: 'new-conversation',
        message: 'Starting a new conversation. How can I assist you?',
        sender: 'assistant',
        timestamp: new Date(),
      }]);
      setError(null);
    } catch (err) {
      console.error('Error starting new conversation:', err);
      setError(formatErrorMessage(err));
    }
  };

  return (
    <div className="chat-interface-container">
      <div className="chat-header">
        <div className="chat-title">AI Assistant</div>
        <button
          onClick={startNewConversation}
          className="new-conversation-btn"
          aria-label="Start new conversation"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          New Chat
        </button>
      </div>

      <div className="chat-messages-container">
        <MessageList
          messages={messages}
          isLoading={isLoading}
          error={error}
        />
      </div>

      <MessageInput
        placeholder="Type your message here..."
        onSend={handleSend}
      />

      <style jsx>{`
        .chat-interface-container {
          display: flex;
          flex-direction: column;
          height: 500px;
          width: 100%;
          max-width: 800px;
          margin: 20px auto;
          border-radius: 16px;
          overflow: hidden;
          background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.1) 100%);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
          border: 1px solid rgba(255, 255, 255, 0.2);
          box-shadow:
            0 8px 32px rgba(31, 38, 135, 0.2),
            0 4px 30px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
          transition: all 0.3s ease;
        }

        .chat-interface-container:hover {
          box-shadow:
            0 12px 40px rgba(31, 38, 135, 0.25),
            0 6px 35px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
        }

        .chat-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 20px;
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        }

        .chat-title {
          font-size: 18px;
          font-weight: 600;
          color: var(--neutral-black);
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .new-conversation-btn {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 8px 16px;
          background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
          color: white;
          border: none;
          border-radius: 24px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
          transition: all 0.3s ease;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .new-conversation-btn:hover {
          background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .new-conversation-btn:active {
          transform: translateY(0);
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }

        .chat-messages-container {
          flex: 1;
          overflow-y: auto;
        }

        @media (max-width: 768px) {
          .chat-interface-container {
            height: 500px;
            margin: 20px 10px;
            border-radius: 12px;
          }

          .chat-header {
            padding: 14px 16px;
          }

          .chat-title {
            font-size: 16px;
          }

          .new-conversation-btn {
            padding: 7px 14px;
            font-size: 13px;
          }
        }

        @media (max-width: 480px) {
          .chat-interface-container {
            height: 400px;
            margin: 10px 5px;
            border-radius: 10px;
          }

          .chat-header {
            flex-direction: column;
            gap: 10px;
            align-items: flex-start;
          }

          .new-conversation-btn {
            width: 100%;
            justify-content: center;
          }
        }
      `}</style>
    </div>
  );
};

export default ChatInterface;