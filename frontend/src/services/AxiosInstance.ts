import axios from "axios";

const API_URL = process.env.REACT_APP_BACKEND_URL;

/**
 * Creates axios instance.
 */
const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // withCredentials: true
});

/**
 * Sets JWT-Token as default Auth Header, if available.
 */
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
