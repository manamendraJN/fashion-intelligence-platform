import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  // Get model info
  getModelInfo: async () => {
    try {
      const response = await api.get('/model-info');
      return response.data;
    } catch (error) {
      console.error('Failed to get model info:', error);
      throw error;
    }
  },

  // Predict measurements from images
  predictMeasurements: async (frontImage, sideImage) => {
    try {
      const formData = new FormData();
      formData.append('front_image', frontImage);
      formData.append('side_image', sideImage);

      const response = await api.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Prediction failed:', error);
      throw error;
    }
  },

  // Preview mask before analysis
  previewMask: async (imageFile) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await api.post('/preview-mask', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Preview failed:', error);
      throw error;
    }
  },

  // Complete analysis (all-in-one)
  completeAnalysis: async (frontImage, sideImage, weightKg, gender) => {
    try {
      const formData = new FormData();
      formData.append('front_image', frontImage);
      formData.append('side_image', sideImage);
      if (weightKg) formData.append('weight_kg', weightKg);
      formData.append('gender', gender);

      const response = await api.post('/complete-analysis', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Complete analysis failed:', error);
      throw error;
    }
  },

  // Save measurements to database
  saveMeasurements: async (data) => {
    try {
      const response = await api.post('/api/size/measurements/save', data);
      return response.data;
    } catch (error) {
      console.error('Failed to save measurements:', error);
      throw error;
    }
  },

  // Get latest measurements
  getLatestMeasurements: async (userIdentifier = 'default', maxAgeDays = 90) => {
    try {
      const response = await api.get('/api/size/measurements/latest', {
        params: {
          user_identifier: userIdentifier,
          max_age_days: maxAgeDays
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to get latest measurements:', error);
      throw error;
    }
  },

  // Get measurement history
  getMeasurementHistory: async (userIdentifier = 'default') => {
    try {
      const response = await api.get('/api/size/measurements/history', {
        params: {
          user_identifier: userIdentifier
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to get measurement history:', error);
      throw error;
    }
  },
};

export default api;