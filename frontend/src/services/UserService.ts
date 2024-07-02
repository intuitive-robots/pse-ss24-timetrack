import axiosInstance from "./AxiosInstance";
import { User } from "../interfaces/User";
import axios from "axios";

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

export { getHiwis };