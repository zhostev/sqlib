// utils/api.js
import axios from 'axios';

// Set up a base URL for axios if you have a common part for all endpoints
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3000/api';

// Create an axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  // You can add more default settings here
  // headers: { 'X-Custom-Header': 'foobar' },
});

// Example API call to get the configuration schema
export const fetchConfigSchema = async () => {
  try {
    const response = await api.get('/schema/config');
    return response.data;
  } catch (error) {
    // Handle the error as you prefer, maybe throw it again or return a default value
    throw error;
  }
};

// Example API call to get the configuration
export const fetchConfig = async () => {
  try {
    const response = await api.get('/config');
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Example API call to save the configuration
export const saveConfig = async (configData) => {
  try {
    const response = await api.post('/config', configData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Example API call to initiate data processing
export const initiateDataProcessing = async () => {
  try {
    const response = await api.post('/data/initiate');
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Example API call to get data processing history
export const fetchDataHistory = async () => {
  try {
    const response = await api.get('/data/history');
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Example API call to get evaluation results
export const fetchEvaluationResults = async () => {
  try {
    const response = await api.get('/evaluation/results');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;