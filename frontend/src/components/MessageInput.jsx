// frontend/src/components/MessageInput.jsx
import React, { useState } from 'react';

const MessageInput = ({ placeholder, onSend }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSend(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder || "Type your message here..."}
          className="message-textarea"
          rows="1"
        />
        <button
          type="submit"
          className="send-button"
          disabled={!inputValue.trim()}
          aria-label="Send message"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>

      <style jsx>{`
        .message-input-container {
          padding: 16px;
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          border-top: 1px solid rgba(255, 255, 255, 0.15);
        }

        .input-wrapper {
          display: flex;
          align-items: flex-end;
          gap: 10px;
          background: rgba(255, 255, 255, 0.9);
          border-radius: 24px;
          padding: 8px 16px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
          transition: all 0.3s ease;
          border: 1px solid rgba(0, 0, 0, 0.05);
        }

        .input-wrapper:focus-within {
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
          border-color: var(--primary-300);
        }

        .message-textarea {
          flex: 1;
          border: none;
          resize: none;
          background: transparent;
          font-size: 15px;
          padding: 8px 0;
          color: var(--neutral-dark);
          max-height: 120px;
          outline: none;
          line-height: 1.5;
        }

        .message-textarea::placeholder {
          color: var(--neutral-gray);
        }

        .send-button {
          background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
          color: white;
          border: none;
          border-radius: 50%;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.3s ease;
          flex-shrink: 0;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }

        .send-button:hover:not(:disabled) {
          background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
          transform: translateY(-2px);
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        }

        .send-button:active:not(:disabled) {
          transform: translateY(0);
        }

        .send-button:disabled {
          background: var(--neutral-gray);
          cursor: not-allowed;
          transform: none;
          box-shadow: none;
        }

        @media (max-width: 768px) {
          .message-input-container {
            padding: 12px;
          }

          .input-wrapper {
            padding: 6px 12px;
            border-radius: 20px;
          }

          .message-textarea {
            font-size: 14px;
            padding: 6px 0;
          }

          .send-button {
            width: 32px;
            height: 32px;
          }
        }
      `}</style>
    </form>
  );
};

export default MessageInput;