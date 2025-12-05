import axios from 'axios';
import { BASE_URL } from '../config/api-config.js';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
});

apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(error)
);
