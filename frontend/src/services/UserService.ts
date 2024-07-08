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

export {
  getHiwis,
  getUsersByRole
};