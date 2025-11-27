export interface GameStats {
  lines_of_code: number
  tests_passed: number
  bugs_fixed: number
  projects_completed: number
  study_hours: number
  exercises_solved: number
}

export interface Rank {
  level: number
  name: string
  emoji: string
}

export interface GameState {
  player_name: string
  level: number
  xp: number
  total_xp_earned: number
  current_module: number
  current_tema: number
  completed_missions: string[]
  unlocked_achievements: string[]
  unlocked_technologies: string[]
  stats: GameStats
  created_at: string
  last_played: string
  play_time_minutes: number
  current_rank?: Rank
  next_rank?: Rank
  xp_for_next_level?: number
}

export interface Mission {
  id: string
  title: string
  description: string
  module: number
  tema: number
  xp_reward: number
  requirements: string[]
  is_completed: boolean
  is_available: boolean
}

export interface Achievement {
  key: string
  name: string
  description: string
  emoji: string
  is_unlocked: boolean
}
