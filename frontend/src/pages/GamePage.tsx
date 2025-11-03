import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { gameApi } from '@/services/api'
import { Trophy, Star, Zap, Code2, CheckCircle2, Lock } from 'lucide-react'

export default function GamePage() {
  const queryClient = useQueryClient()

  const { data: gameState } = useQuery({
    queryKey: ['gameState'],
    queryFn: gameApi.getGameState,
  })

  const { data: missions } = useQuery({
    queryKey: ['missions'],
    queryFn: gameApi.getMissions,
  })

  const { data: achievements } = useQuery({
    queryKey: ['achievements'],
    queryFn: gameApi.getAchievements,
  })

  const completeMissionMutation = useMutation({
    mutationFn: (missionId: string) => gameApi.completeMission(missionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['gameState'] })
      queryClient.invalidateQueries({ queryKey: ['missions'] })
      queryClient.invalidateQueries({ queryKey: ['achievements'] })
    },
  })

  if (!gameState) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  const xpPercentage = ((gameState.xp / (gameState.xp_for_next_level || 1)) * 100).toFixed(0)

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold text-gray-900 mb-2">
          🎮 DATA ENGINEER: THE GAME
        </h1>
        <p className="text-xl text-gray-600">
          Aprende mientras juegas. Completa misiones y sube de nivel.
        </p>
      </div>

      {/* Player Info */}
      <div className="card bg-gradient-to-r from-primary-50 to-secondary-50">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">
              👤 {gameState.player_name}
            </h2>
            <p className="text-lg text-gray-700">
              {gameState.current_rank?.emoji} {gameState.current_rank?.name}
            </p>
          </div>
          <div className="text-right">
            <p className="text-5xl font-bold text-primary">
              Nivel {gameState.level}
            </p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-sm text-gray-700">
            <span>
              XP: {gameState.xp.toLocaleString()} / {gameState.xp_for_next_level?.toLocaleString()}
            </span>
            <span>{xpPercentage}%</span>
          </div>
          <div className="progress-bar h-4">
            <div
              className="progress-fill bg-gradient-to-r from-primary to-secondary"
              style={{ width: `${xpPercentage}%` }}
            />
          </div>
        </div>

        {gameState.next_rank && (
          <p className="text-sm text-gray-600 mt-4 text-center">
            Próximo rango: {gameState.next_rank.emoji} {gameState.next_rank.name} (Nivel{' '}
            {gameState.next_rank.level})
          </p>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <Code2 className="w-8 h-8 text-primary" />
            <span className="text-3xl font-bold text-gray-900">
              {gameState.stats.lines_of_code.toLocaleString()}
            </span>
          </div>
          <p className="text-gray-600">Líneas de código</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <CheckCircle2 className="w-8 h-8 text-green-500" />
            <span className="text-3xl font-bold text-gray-900">
              {gameState.stats.tests_passed}
            </span>
          </div>
          <p className="text-gray-600">Tests pasados</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <Trophy className="w-8 h-8 text-yellow-500" />
            <span className="text-3xl font-bold text-gray-900">
              {gameState.stats.projects_completed}
            </span>
          </div>
          <p className="text-gray-600">Proyectos completados</p>
        </div>
      </div>

      {/* Missions */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">🚀 Misiones Disponibles</h2>
        <div className="space-y-4">
          {missions?.map((mission) => (
            <div
              key={mission.id}
              className={`card ${
                mission.is_completed
                  ? 'bg-green-50 border border-green-200'
                  : mission.is_available
                  ? 'hover:shadow-lg transition-shadow'
                  : 'opacity-50'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    {mission.is_completed ? (
                      <CheckCircle2 className="w-6 h-6 text-green-500" />
                    ) : mission.is_available ? (
                      <Star className="w-6 h-6 text-primary" />
                    ) : (
                      <Lock className="w-6 h-6 text-gray-400" />
                    )}
                    <h3 className="text-xl font-semibold text-gray-900">
                      {mission.title}
                    </h3>
                  </div>
                  <p className="text-gray-600 mb-3 ml-9">{mission.description}</p>
                  <div className="flex items-center space-x-4 ml-9 text-sm">
                    <span className="text-gray-600">
                      Módulo {mission.module} - Tema {mission.tema}
                    </span>
                    <span className="flex items-center text-primary font-medium">
                      <Zap className="w-4 h-4 mr-1" />
                      +{mission.xp_reward} XP
                    </span>
                  </div>
                </div>
                {!mission.is_completed && mission.is_available && (
                  <button
                    onClick={() => completeMissionMutation.mutate(mission.id)}
                    disabled={completeMissionMutation.isPending}
                    className="btn btn-primary"
                  >
                    {completeMissionMutation.isPending ? 'Completando...' : 'Completar'}
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">🏆 Logros</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {achievements?.map((achievement) => (
            <div
              key={achievement.key}
              className={`card ${
                achievement.is_unlocked
                  ? 'bg-gradient-to-br from-yellow-50 to-orange-50 border border-yellow-200'
                  : 'opacity-50'
              }`}
            >
              <div className="text-center">
                <div className="text-4xl mb-2">{achievement.emoji}</div>
                <h3 className="font-bold text-gray-900">{achievement.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{achievement.description}</p>
                {achievement.is_unlocked && (
                  <span className="badge badge-success mt-2">Desbloqueado</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Technologies */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">🔧 Tecnologías Desbloqueadas</h2>
        <div className="card">
          <div className="flex flex-wrap gap-2">
            {gameState.unlocked_technologies.map((tech) => (
              <span key={tech} className="badge badge-info text-base px-4 py-2">
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
