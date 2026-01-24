// frontend/src/services/apiService.js
import { NEXT_PUBLIC_API_URL } from '../utils/constants';

/**
 * Service module for handling API communications with the backend
 */

const API_BASE_URL = NEXT_PUBLIC_API_URL;

/**
 * Sends a chat message to the backend API
 * @param {string} userId - The authenticated user's ID
 * @param {string} message - The user's message to send
 * @param {string} [conversationId] - Optional conversation ID to continue a conversation
 * @returns {Promise<Object>} The API response containing the assistant's reply
 */
export const sendChatMessage = async (userId, message, conversationId = null) => {
  // Validate userId
  if (!userId) {
    throw new Error('User ID is required to send a message');
  }

  try {
    const requestBody = {
      message,
    };

    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }

    const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      // Handle different error statuses
      if (response.status === 400) {
        throw new Error('Bad request: Invalid message format');
      } else if (response.status === 401) {
        throw new Error('Unauthorized: Please sign in to continue');
      } else if (response.status === 403) {
        throw new Error('Forbidden: Access denied');
      } else if (response.status === 500) {
        throw new Error('Server error: Unable to process your request');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Gets conversation history (if needed)
 * @param {string} userId - The authenticated user's ID
 * @param {string} conversationId - The conversation ID to retrieve
 * @returns {Promise<Object>} The conversation data
 */
export const getConversationHistory = async (userId, conversationId) => {
  // Validate userId and conversationId
  if (!userId) {
    throw new Error('User ID is required to get conversation history');
  }
  if (!conversationId) {
    throw new Error('Conversation ID is required to get conversation history');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting conversation history:', error);
    throw error;
  }
};

/**
 * Creates a new conversation
 * @param {string} userId - The authenticated user's ID
 * @returns {Promise<Object>} The conversation data
 */
export const createNewConversation = async (userId) => {
  // Validate userId
  if (!userId) {
    throw new Error('User ID is required to create a new conversation');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating new conversation:', error);
    throw error;
  }
};