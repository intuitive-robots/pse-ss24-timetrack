import axiosInstance from "./AxiosInstance";
import {handleAxiosError} from "../utils/AxiosUtils";

/**
 * Attempts to log in a user using the provided username and password.
 * If successful, stores the user's access token in localStorage.
 *
 * @param username - The username of the user trying to log in.
 * @param password - The password of the user trying to log in.
 * @returns The response data from the login request which includes the access token.
 * @throws An error if the login request fails.
 */
const login = async (username: string, password: string) => {
  try {
    const response = await axiosInstance.post('/user/login', { username, password });
    if (response.data.accessToken) {
      const tokenValue = response.data.accessToken;
      localStorage.setItem('token', tokenValue);
    }
    return response.data;
  } catch (error) {
    console.error('Login failed', error);
    handleAxiosError(error);
  }
};

/**
 * Retrieves the profile information of the currently logged-in user.
 * Requires an authentication token to be set in the headers.
 *
 * @returns The profile data of the user if retrieval is successful.
 * @throws An error if the profile cannot be retrieved due to network issues or missing authorization.
 */
const getProfile = async () => {
  try {
    const response = await axiosInstance.get('user/getProfile');
    return response.data;
  } catch (error) {
    console.error('Profile could not be retrieved', error);
    handleAxiosError(error);
  }
};

/**
 * Logs out the current user by removing the user's access token from localStorage.
 * It also makes a logout request to the server to invalidate the session.
 */
const logout = async () => {
  try {
    await axiosInstance.post('user/logout');
    localStorage.removeItem('token');
  } catch (error) {
    console.error('Logout failed', error);
    handleAxiosError(error);
  }
};

/**
 * Fetches all users from the backend.
 * Requires an authentication token to be set in the headers.
 *
 * @returns The list of users if retrieval is successful.
 * @throws An error if the users cannot be retrieved due to network issues or missing authorization.
 */
const getUsers = async () => {
  try {
    const response = await axiosInstance.get('user/getUsers');
    return response.data;
  } catch (error) {
    console.error('Users could not be retrieved', error);
    handleAxiosError(error);
  }
};

/**
 * Resets the password for a specified user.
 *
 * @param {string} newPassword - The new password for the user.
 * @returns {Promise<any>} - The response from the backend after attempting to reset the password.
 * @throws {Error} - Throws an error if the password reset request fails.
 */
const resetPassword = async (newPassword: string): Promise<any> => {
  try {
    const response = await axiosInstance.post('/user/resetPassword', {
      password: newPassword
    });
    return response.data;
  } catch (error) {
    console.error('Password reset failed:', error);
    handleAxiosError(error);
  }
};

export { login, getProfile, logout, getUsers, resetPassword };
