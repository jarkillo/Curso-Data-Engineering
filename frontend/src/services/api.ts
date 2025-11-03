import axios from 'axios'
import type { Module, ModuleSummary, ContentResponse } from '../types/content'
import type { GameState, Mission, Achievement } from '../types/game'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

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

  completeMission: async (missionId: string): Promise<GameState> => {
    const { data } = await api.post(`/game/mission/${missionId}/complete`)
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

export default api
