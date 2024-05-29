import axios from 'axios';

const API_URL = 'http://localhost:5000';

/**
 * Creates axios instance.
 */
const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Sets JWT-Token as default Auth Header, if available.
 */
axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!).accessToken : null;
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default axiosInstance;
