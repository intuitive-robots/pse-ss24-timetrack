import axiosInstance from "./AxiosInstance";
import { User } from "../interfaces/User";

const getHiwis = async (username: string) => {
  try {
    const response = await axiosInstance.get('/user/getHiwis', {
      params: { username } });
    return response.data;
  } catch (error) {
    console.error('Fetching hiwis by username failed');
    throw error;
  }
};
const getUsersByRole = async (role: string) => {
  try {
    const response = await axiosInstance.get('/user/getUsersByRole', {
      params: { role } });
    return response.data;
  } catch (error) {
    console.error('Fetching users by role failed');
    throw error;
  }
};

/**
 * Deletes a user by their username.
 *
 * @param {string} username - The username of the user to be deleted.
 * @returns {Promise<any>} The response data from the backend.
 */
const deleteUser = async (username: string) => {
  try {
    const response = await axiosInstance.delete('/user/deleteUser', {
      data: { username }
    });
    return response.data;
  } catch (error) {
    console.error('Deleting user failed', error);
    throw error;
  }
};

/**
 * Creates a new user with provided user details.
 * @param userData The data of the user to be created.
 * @returns The response data from the backend.
 */
const createUser = async (userData: User): Promise<any> => {
    try {
        const response = await axiosInstance.post('/user/createUser', userData);
        return response.data;
    } catch (error) {
        console.error('Creating user failed', error);
        throw error;
    }
};

/**
 * Fetches supervisor details for the currently authenticated user.
 * Handles different logic based on the user role (HIWI or SECRETARY).
 *
 * @returns {Promise<any>} The response data from the backend containing supervisor details or an error message.
 */
const getSupervisor = async (): Promise<any> => {
    try {
        const response = await axiosInstance.get('user/getSupervisor');
        return response.data;
    } catch (error) {
        console.error('Fetching supervisor failed', error);
        throw error;
    }
};

/**
 * Retrieves all supervisors from the backend.
 *
 * @returns {Promise<User[]>} A promise that resolves to an array of User objects representing the supervisors.
 */
const getSupervisors = async (): Promise<User[]> => {
    try {
        const response = await axiosInstance.get('/user/getSupervisors');
        return response.data;
    } catch (error: any) {
        console.error('Error fetching supervisors:', error.response?.data || error.message);
        throw new Error(error.response?.data || "Failed to fetch supervisors.");
    }
};

export { getHiwis, getUsersByRole, deleteUser, createUser, getSupervisor, getSupervisors };