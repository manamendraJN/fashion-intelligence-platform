import axios from 'axios';
import { PredictionResult } from './types';

const API_BASE_URL = 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export const predictImage = async (file: File): Promise<PredictionResult> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post<PredictionResult>('/predict', formData);
  return response.data;
};

export const generateHairStyle = async (file: File, prompt: string): Promise<{ success: boolean; recommendation: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('prompt', prompt);
  
  const response = await apiClient.post<{ success: boolean; recommendation: string }>('/generate-hair', formData);
  return response.data;
};

export const analyzeNails = async (file: File, prompt: string): Promise<{ success: boolean; recommendation: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('prompt', prompt);
  const response = await apiClient.post<{ success: boolean; recommendation: string }>('/analyze-nail', formData);
  return response.data;
};

export const analyzeDental = async (file: File, prompt: string): Promise<{ success: boolean; recommendation: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('prompt', prompt);
  const response = await apiClient.post<{ success: boolean; recommendation: string }>('/analyze-dental', formData);
  return response.data;
};

export const checkHealth = async (): Promise<boolean> => {
  try {
    await apiClient.get('/health');
    return true;
  } catch {
    return false;
  }
};
