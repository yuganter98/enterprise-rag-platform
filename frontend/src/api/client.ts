import axios from 'axios';

const client = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

client.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// If the token is missing, expired or invalid, drop it and send the user to login.
client.interceptors.response.use(
    (response) => response,
    (error) => {
        const isLoginRequest = error.config?.url?.includes('/login/access-token');
        if (error.response?.status === 401 && !isLoginRequest) {
            localStorage.removeItem('token');
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default client;
