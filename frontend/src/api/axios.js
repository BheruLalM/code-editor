import axios from 'axios';
import { useAdminStore } from '../store/adminStore';
import { getApiBaseUrl } from './baseUrl';

const api = axios.create({
    baseURL: getApiBaseUrl(),
    timeout: 15000,
});

api.interceptors.request.use((config) => {
    const token = useAdminStore.getState().token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            useAdminStore.getState().logout();
            window.location.href = '/admin/login';
        }
        return Promise.reject(error);
    }
);

export default api;
