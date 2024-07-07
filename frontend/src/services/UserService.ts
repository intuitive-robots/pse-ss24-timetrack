import axiosInstance from "./AxiosInstance";
import {User} from "../interfaces/User";

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

export { getHiwis, deleteUser, createUser };