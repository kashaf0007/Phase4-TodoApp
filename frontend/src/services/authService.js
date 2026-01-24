// frontend/src/services/authService.js
import { signIn, signOut, useSession } from 'better-auth/react';

/**
 * Authentication service module for handling user authentication
 */

/**
 * Signs in a user with the provided credentials
 * @param {Object} credentials - User credentials (email, password, etc.)
 * @returns {Promise<Object>} Sign in result
 */
export const authenticateUser = async (credentials) => {
  try {
    const result = await signIn('credentials', {
      ...credentials,
      redirect: false, // Prevent automatic redirect
    });
    
    return result;
  } catch (error) {
    console.error('Authentication error:', error);
    throw error;
  }
};

/**
 * Signs out the current user
 * @returns {Promise<void>}
 */
export const logoutUser = async () => {
  try {
    await signOut({ redirect: false }); // Prevent automatic redirect
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};

/**
 * Gets the current user session
 * @returns {Object} Session information
 */
export const getCurrentSession = () => {
  return useSession();
};

/**
 * Checks if a user is currently authenticated
 * @returns {boolean} True if user is authenticated, false otherwise
 */
export const isAuthenticated = () => {
  const session = useSession();
  return !!session.data?.user;
};