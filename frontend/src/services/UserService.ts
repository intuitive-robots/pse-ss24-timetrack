import axiosInstance from "./AxiosInstance";
import { User } from "../interfaces/User";
import {handleAxiosError} from "../utils/AxiosUtils";
import {ContractInfo} from "../interfaces/ContractInfo";

const getHiwis = async () => {
  try {
    const response = await axiosInstance.get('/user/getHiwis');
    return response.data;
  } catch (error) {
    console.error('Fetching hiwis by username failed');
    handleAxiosError(error);
  }
};
const getUsersByRole = async (role: string) => {
  try {
    const response = await axiosInstance.get('/user/getUsersByRole', {
      params: { role } });
    return response.data;
  } catch (error) {
    console.error('Fetching users by role failed');
    handleAxiosError(error);
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
    handleAxiosError(error);
  }
};

/**
 * Archives a user by their username.
 *
 * @param {string} username - The username of the user to be deleted.
 * @returns {Promise<any>} The response data from the backend.
 */
const archiveUser = async (username: string) => {
  try {
    const response = await axiosInstance.post('/user/archiveUser', username);
    return response.data;
  } catch (error) {
    console.error('Archiving user failed', error);
    handleAxiosError(error);
  }
};

/**
 * Archives a user by their username.
 *
 * @param {string} username - The username of the user to be deleted.
 * @returns {Promise<any>} The response data from the backend.
 */
const unarchiveUser = async (username: string) => {
  try {
    const response = await axiosInstance.post('/user/unarchiveUser', username);
    return response.data;
  } catch (error) {
    console.error('Unarchiving user failed', error);
    handleAxiosError(error);
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
        handleAxiosError(error);
    }
};

/**
 * Updates an existing user with provided user details.
 * @param userData The data of the user to be updated.
 * @returns The response data from the backend.
 */
const updateUser = async (userData: User): Promise<any> => {
    try {
        console.log(userData);
        const response = await axiosInstance.post(`/user/updateUser`, userData);
        return response.data;
    } catch (error) {
        console.error('Updating user failed', error);
        handleAxiosError(error);
    }
};


/**
 * Fetches supervisor details for the currently authenticated user.
 * Handles different logic based on the user role (HIWI or SECRETARY).
 *
 * @returns {Promise<any>} The response data from the backend containing supervisor details or an error message.
 */
const getHiwiSupervisor = async (): Promise<any> => {
    try {
        const response = await axiosInstance.get('/user/getSupervisor');
        return response.data;
    } catch (error) {
        console.error('Fetching supervisor failed', error);
        throw error;
    }
};

const getSupervisor = async (username: string) : Promise<any> => {
    try {
        const response = await axiosInstance.get('/user/getSupervisor', {
            params: { username }
        });
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

/**
 * Fetches contract information for a specific user.
 *
 * @param {string} username - The username of the user whose contract information is to be fetched.
 * @returns {Promise<ContractInfo>} The response data from the backend containing the contract information.
 */
const getContractInfo = async (username: string): Promise<ContractInfo> => {
  try {
    const response = await axiosInstance.get('user/getContractInfo', {
      params: { username }
    });
    return response.data as ContractInfo;
  } catch (error) {
    console.error('Fetching contract information failed', error);
    handleAxiosError(error);
    throw error;
  }
};

/**
 * Retrieves all archived users from the backend.
 *
 * @returns {Promise<User[]>} A promise that resolves to an array of User objects representing the archived users.
 */
const getArchivedUsers = async (): Promise<User[]> => {
    try {
        const response = await axiosInstance.get('/user/getArchivedUsers');
        return response.data;
    } catch (error: any) {
        console.error('Error fetching archived users:', error.response?.data || error.message);
        throw new Error(error.response?.data || "Failed to fetch archived users.");
    }
};

export { getHiwis, getUsersByRole, deleteUser, archiveUser, unarchiveUser, createUser, getSupervisor, getHiwiSupervisor, getSupervisors, updateUser, getContractInfo, getArchivedUsers };