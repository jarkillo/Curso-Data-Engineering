export interface Topic {
  id: string
  number: number
  title: string
  description?: string
  completed: boolean
  coverage?: number
  available_sections: string[]
}

export interface Module {
  id: string
  number: number
  title: string
  description?: string
  status: 'completed' | 'in_progress' | 'locked'
  progress_percentage: number
  topics: Topic[]
}

export interface ModuleSummary {
  id: string
  number: number
  title: string
  description?: string
  status: 'completed' | 'in_progress' | 'locked'
  progress_percentage: number
  topic_count: number
}

export interface ContentResponse {
  module_id: string
  topic_id: string
  section: string
  content: string
  metadata?: Record<string, any>
}
