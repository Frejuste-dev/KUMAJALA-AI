import axios from 'axios';

// URL de production du backend
const API_BASE_URL = 'https://kumajala-backend.onrender.com/kumajala-api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('Erreur de l\'API:', error.response || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;
