import axios from 'axios';

// Remplacez cette URL par celle fournie par Railway après le déploiement
const API_URL = 'https://your-railway-app-url';  

const api = axios.create({
    baseURL: API_URL,
});

export const registerUser = (userData) => api.post('/register', userData);
export const loginUser = (userData) => api.post('/login', userData);
export const uploadDocument = (formData, token) => api.post('/upload', formData, {
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
    },
});
export const checkStatus = (token) => api.get('/check-status', {
    headers: {
        'Authorization': `Bearer ${token}`,
    },
});
