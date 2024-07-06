import axiosInstance from "./AxiosInstance";

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
    const response = await axiosInstance.delete('/user/delete', {
      data: { username }
    });
    return response.data;
  } catch (error) {
    console.error('Deleting user failed', error);
    throw error;
  }
};

export { getHiwis, deleteUser };