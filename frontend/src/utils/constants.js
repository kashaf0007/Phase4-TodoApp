// frontend/src/utils/constants.js

// API Configuration
export const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Chat Configuration
export const CHAT_DEFAULT_USER_NAME = 'User';
export const CHAT_ASSISTANT_NAME = 'AI Assistant';
export const CHAT_MAX_MESSAGE_LENGTH = 2000;

// UI Configuration
export const UI_DEFAULT_PAGE_TITLE = 'Todo App - Chat Interface';
export const UI_LOADING_MESSAGE = 'Thinking...';
export const UI_ERROR_MESSAGE = 'Sorry, something went wrong. Please try again.';

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.',
  INVALID_RESPONSE: 'Invalid response from server.',
  AUTHENTICATION_ERROR: 'Authentication required. Please sign in.',
};

// Status Codes
export const STATUS_CODES = {
  SUCCESS: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
};

// Event Types
export const EVENT_TYPES = {
  MESSAGE_SENT: 'message_sent',
  MESSAGE_RECEIVED: 'message_received',
  CONNECTION_OPENED: 'connection_opened',
  CONNECTION_CLOSED: 'connection_closed',
  ERROR_OCCURRED: 'error_occurred',
};