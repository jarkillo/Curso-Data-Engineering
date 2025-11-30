import axios from 'axios'
import type { Module, ModuleSummary, ContentResponse } from '../types/content'
import type { GameState, Mission, Achievement, MissionResult } from '../types/game'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types/auth'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Content API
export const contentApi = {
  getModules: async (): Promise<ModuleSummary[]> => {
    const { data } = await api.get('/modules')
    return data
  },

  getModule: async (moduleId: string): Promise<Module> => {
    const { data } = await api.get(`/modules/${moduleId}`)
    return data
  },

  getContent: async (
    moduleId: string,
    topicId: string,
    section: string
  ): Promise<ContentResponse> => {
    const { data } = await api.get(`/content/${moduleId}/${topicId}/${section}`)
    return data
  },
}

// Game API
export const gameApi = {
  getGameState: async (): Promise<GameState> => {
    const { data } = await api.get('/game/state')
    return data
  },

  getMissions: async (): Promise<Mission[]> => {
    const { data } = await api.get('/game/missions')
    return data
  },

  getAchievements: async (): Promise<Achievement[]> => {
    const { data } = await api.get('/game/achievements')
    return data
  },

  completeMission: async (missionId: string, answers: number[]): Promise<MissionResult> => {
    const { data } = await api.post(`/game/mission/${missionId}/complete`, { answers })
    return data
  },

  addXP: async (amount: number, reason?: string): Promise<GameState> => {
    const { data } = await api.post('/game/xp', { amount, reason })
    return data
  },
}

// Progress API
export const progressApi = {
  getProgress: async () => {
    const { data } = await api.get('/progress')
    return data
  },
}

// Auth API
export const authApi = {
  register: async (data: RegisterRequest): Promise<User> => {
    const { data: user } = await api.post('/auth/register', data)
    return user
  },

  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const { data: response } = await api.post('/auth/login', data)
    return response
  },

  getMe: async (token: string): Promise<User> => {
    const { data: user } = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return user
  },

  logout: () => {
    localStorage.removeItem('token')
  },
}

export default api
