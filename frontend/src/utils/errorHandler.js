// frontend/src/utils/errorHandler.js
import React from 'react';

/**
 * Error handling utilities for the frontend application
 */

/**
 * Formats error messages for display to users
 * @param {Error|string} error - The error to format
 * @returns {string} A user-friendly error message
 */
export const formatErrorMessage = (error) => {
  if (typeof error === 'string') {
    return error;
  }

  if (error && error.message) {
    // Handle network errors
    if (error.message.includes('Failed to fetch')) {
      return 'Unable to connect to the server. Please check your internet connection.';
    }

    // Handle timeout errors
    if (error.message.includes('timeout')) {
      return 'Request timed out. Please try again.';
    }

    return error.message;
  }

  return 'An unexpected error occurred. Please try again.';
};

/**
 * Logs error to console with additional context
 * @param {Error} error - The error to log
 * @param {string} context - Context where the error occurred
 */
export const logError = (error, context = '') => {
  console.group(`❌ Error in ${context || 'unknown context'}`);
  console.error(error);
  console.groupEnd();
};

/**
 * Handles API errors and returns appropriate user-facing messages
 * @param {Response} response - The fetch response object
 * @returns {Promise<Object>} Object with success status and message
 */
export const handleApiError = async (response) => {
  const errorData = {
    success: false,
    message: '',
    status: response.status,
  };

  try {
    const responseBody = await response.text();
    const parsedBody = responseBody ? JSON.parse(responseBody) : {};

    switch (response.status) {
      case 400:
        errorData.message = parsedBody.error || 'Bad request. Please check your input.';
        break;
      case 401:
        errorData.message = 'Unauthorized. Please sign in to continue.';
        break;
      case 403:
        errorData.message = 'Access forbidden. You do not have permission to perform this action.';
        break;
      case 404:
        errorData.message = 'Resource not found.';
        break;
      case 500:
        errorData.message = 'Server error. Please try again later.';
        break;
      default:
        errorData.message = parsedBody.error || `Request failed with status ${response.status}`;
    }
  } catch (parseError) {
    // If we can't parse the error response, use generic message
    errorData.message = `Request failed with status ${response.status}`;
  }

  return errorData;
};

/**
 * Generic error boundary component for React
 */
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    logError(error, 'ErrorBoundary');
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <p>{this.state.error?.toString()}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}