import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  register: (data: { email: string; username: string; password: string }) =>
    api.post('/auth/register', data),
  
  login: (email: string, password: string) =>
    api.post('/auth/login', null, { params: { email, password } }),
  
  getCurrentUser: () => api.get('/auth/me'),
}

// Content API
export const contentAPI = {
  upload: (formData: FormData) =>
    api.post('/content/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  
  getContent: (contentId: string) => api.get(`/content/${contentId}`),
  
  listContent: () => api.get('/content'),
  
  getAdaptations: (contentId: string) =>
    api.get(`/content/${contentId}/adaptations`),
}

// Distribution API
export const distributionAPI = {
  distribute: (data: {
    content_id: string
    platforms: string[]
    scheduled_time?: string
    immediate: boolean
  }) => api.post('/distribute', data),
  
  getStatus: (jobId: string) => api.get(`/distribute/${jobId}`),
}

// Analytics API
export const analyticsAPI = {
  getContentAnalytics: (contentId: string) =>
    api.get(`/analytics/${contentId}`),
  
  getTrends: (niche: string) =>
    api.post('/analytics/trends', null, { params: { niche } }),
}

// Monetization API
export const monetizationAPI = {
  analyze: (contentId: string) =>
    api.post(`/monetization/analyze/${contentId}`),
  
  getPlacements: (contentId: string) =>
    api.get(`/monetization/${contentId}/placements`),
}
