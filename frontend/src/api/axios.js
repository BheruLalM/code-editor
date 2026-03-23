import axios from 'axios';
import { useAdminStore } from '../store/adminStore';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
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
