import { create } from 'zustand'
import type { GameState } from '../types/game'

interface GameStore {
  gameState: GameState | null
  setGameState: (state: GameState) => void
  updateXP: (xp: number) => void
}

export const useGameStore = create<GameStore>((set) => ({
  gameState: null,
  setGameState: (state) => set({ gameState: state }),
  updateXP: (xp) =>
    set((state) => ({
      gameState: state.gameState
        ? { ...state.gameState, xp, total_xp_earned: state.gameState.total_xp_earned + xp }
        : null,
    })),
}))
