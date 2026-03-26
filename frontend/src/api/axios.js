import axios from 'axios';
import { useAdminStore } from '../store/adminStore';
import { getApiBaseUrl } from './baseUrl';

const api = axios.create({
    baseURL: getApiBaseUrl(),
    timeout: 15000,
});

// No interceptors needed for auth anymore

export default api;
