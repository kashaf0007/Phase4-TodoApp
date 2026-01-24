// frontend/src/components/MessageList.jsx
import React from 'react';
import ToolCallDisplay from './ToolCallDisplay';

const MessageList = ({ messages, isLoading, error }) => {
  return (
    <div className="message-list-container">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`message-wrapper ${msg.sender}-message-wrapper`}
        >
          <div
            className={`message-bubble ${msg.sender}-message ${msg.isError ? 'error-message' : ''}`}
            role="alert"
            aria-live="polite"
          >
            <div className="message-content">
              {msg.message}

              {/* Display tool calls if present */}
              {msg.toolCalls && msg.toolCalls.length > 0 && (
                <div className="tool-calls-section">
                  <ToolCallDisplay toolCalls={msg.toolCalls} />
                </div>
              )}

              {/* Display confirmation message if present */}
              {msg.confirmation && (
                <div className="confirmation-message">
                  ✓ {msg.confirmation}
                </div>
              )}
            </div>
            <div className="message-timestamp">
              {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
            </div>
          </div>
        </div>
      ))}

      {isLoading && (
        <div className="message-wrapper assistant-message-wrapper">
          <div
            className="message-bubble assistant-message loading-message"
            aria-label="Assistant is thinking"
          >
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="message-wrapper assistant-message-wrapper">
          <div
            className="message-bubble assistant-message error-message"
            role="alert"
            aria-live="assertive"
          >
            <div className="message-content">
              {error}
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .message-list-container {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 16px;
          background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.2) 100%);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
        }

        .message-wrapper {
          display: flex;
          width: 100%;
        }

        .user-message-wrapper {
          justify-content: flex-end;
        }

        .assistant-message-wrapper {
          justify-content: flex-start;
        }

        .message-bubble {
          max-width: 85%;
          border-radius: 18px;
          padding: 16px 20px;
          position: relative;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
          transition: all 0.3s ease;
          animation: fadeInUp 0.3s ease-out;
          display: flex;
          flex-direction: column;
        }

        .message-bubble:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
        }

        .user-message {
          background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
          color: white;
          border-bottom-right-radius: 4px;
        }

        .assistant-message {
          background: rgba(255, 255, 255, 0.85);
          color: var(--neutral-dark);
          border-bottom-left-radius: 4px;
        }

        .error-message {
          background: linear-gradient(135deg, var(--danger-500), var(--danger-600));
          color: white;
        }

        .loading-message {
          background: rgba(255, 255, 255, 0.85);
          padding: 16px;
          display: flex;
          justify-content: center;
          align-items: center;
        }

        .message-content {
          font-size: 15px;
          line-height: 1.5;
          word-wrap: break-word;
        }

        .tool-calls-section {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid rgba(255, 255, 255, 0.2);
        }

        .confirmation-message {
          margin-top: 8px;
          font-size: 13px;
          color: var(--success-600);
          font-weight: 500;
        }

        .message-timestamp {
          font-size: 11px;
          opacity: 0.7;
          margin-top: 6px;
          text-align: right;
          font-style: italic;
        }

        .typing-indicator {
          display: flex;
          justify-content: center;
          gap: 4px;
          padding: 8px 0;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background-color: var(--neutral-gray);
          border-radius: 50%;
          display: inline-block;
          animation: typing 1.4s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(1) {
          animation-delay: -0.32s;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: -0.16s;
        }

        @keyframes typing {
          0%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-5px);
          }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @media (max-width: 768px) {
          .message-bubble {
            max-width: 90%;
            padding: 14px 18px;
          }

          .message-content {
            font-size: 14px;
          }
        }
      `}</style>
    </div>
  );
};

export default MessageList;