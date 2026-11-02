import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;
const API_VERSION = import.meta.env.VITE_API_VERSION;

const api = axios.create({
    baseURL: `${API_URL}/api/${API_VERSION}`,
});

export default api;