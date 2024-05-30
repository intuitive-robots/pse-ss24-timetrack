import axiosInstance from "./AxiosInstance";

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
    const response = await axiosInstance.post('/token', { username, password });
    if (response.data.accessToken) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
  } catch (error) {
    throw new Error('Login failed');
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
    const response = await axiosInstance.get('/profile');
    return response.data;
  } catch (error) {
    console.error('Profile could not be retrieved');
  }
};

/**
 * Logs out the current user by removing the user's access token from localStorage.
 * It also makes a logout request to the server to invalidate the session.
 */
const logout = async () => {
  try {
    await axiosInstance.post('/logout');
    localStorage.removeItem('user');
  } catch (error) {
    console.error('Logout failed');
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
    const response = await axiosInstance.get('/readUsers');
    return response.data;
  } catch (error) {
    console.error('Users could not be retrieved');
    throw error;
  }
};

export { login, getProfile, logout, getUsers};