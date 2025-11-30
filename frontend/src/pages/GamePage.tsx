import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { gameApi } from '@/services/api'
import { Trophy, Star, Zap, Code2, CheckCircle2, Lock, Play, RefreshCw } from 'lucide-react'
import QuizModal from '@/components/game/QuizModal'
import type { Mission } from '@/types/game'

export default function GamePage() {
  const queryClient = useQueryClient()
  const [selectedMission, setSelectedMission] = useState<Mission | null>(null)

  const { data: gameState, isLoading, isError } = useQuery({
    queryKey: ['gameState'],
    queryFn: gameApi.getGameState,
    retry: 1,
  })

  const { data: missions } = useQuery({
    queryKey: ['missions'],
    queryFn: gameApi.getMissions,
    retry: 1,
  })

  const { data: achievements } = useQuery({
    queryKey: ['achievements'],
    queryFn: gameApi.getAchievements,
    retry: 1,
  })

  const completeMissionMutation = useMutation({
    mutationFn: ({ missionId, answers }: { missionId: string; answers: number[] }) =>
      gameApi.completeMission(missionId, answers),
    onSuccess: (result) => {
      if (result.success) {
        queryClient.invalidateQueries({ queryKey: ['gameState'] })
        queryClient.invalidateQueries({ queryKey: ['missions'] })
        queryClient.invalidateQueries({ queryKey: ['achievements'] })
      }
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (isError || !gameState) {
    return (
      <div className="max-w-2xl mx-auto text-center py-16">
        <div className="text-6xl mb-4">🎮</div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          El juego no está disponible
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          No se pudo cargar el estado del juego. Esto puede deberse a un error del servidor.
        </p>
        <button
          onClick={() => window.location.reload()}
          className="btn btn-primary"
        >
          Reintentar
        </button>
      </div>
    )
  }

  const xpPercentage = ((gameState.xp / (gameState.xp_for_next_level || 1)) * 100).toFixed(0)

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-2">
          🎮 DATA ENGINEER: THE GAME
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300">
          Aprende mientras juegas. Completa misiones y sube de nivel.
        </p>
      </div>

      {/* Player Info */}
      <div className="card bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              👤 {gameState.player_name}
            </h2>
            <p className="text-lg text-gray-700 dark:text-gray-300">
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
          <div className="flex justify-between text-sm text-gray-700 dark:text-gray-300">
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
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-4 text-center">
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
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {gameState.stats.lines_of_code.toLocaleString()}
            </span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Líneas de código</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <CheckCircle2 className="w-8 h-8 text-green-500" />
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {gameState.stats.tests_passed}
            </span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Tests pasados</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <Trophy className="w-8 h-8 text-yellow-500" />
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {gameState.stats.projects_completed}
            </span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Proyectos completados</p>
        </div>
      </div>

      {/* Missions */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">🚀 Misiones Disponibles</h2>
        <div className="space-y-4">
          {missions?.map((mission) => (
            <div
              key={mission.id}
              className={`card ${
                mission.is_completed
                  ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
                  : mission.is_available
                  ? 'hover:shadow-lg dark:hover:shadow-gray-800 transition-shadow'
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
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {mission.title}
                    </h3>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 mb-3 ml-9">{mission.description}</p>
                  <div className="flex items-center space-x-4 ml-9 text-sm">
                    <span className="text-gray-600 dark:text-gray-400">
                      Módulo {mission.module} - Tema {mission.tema}
                    </span>
                    <span className="flex items-center text-primary font-medium">
                      <Zap className="w-4 h-4 mr-1" />
                      +{mission.xp_reward} XP
                    </span>
                    <span className="text-gray-500 dark:text-gray-500">
                      {mission.questions.length} preguntas
                    </span>
                  </div>
                </div>
                {mission.is_available && (
                  <button
                    onClick={() => setSelectedMission(mission)}
                    className={`btn ${
                      mission.is_completed
                        ? 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                        : 'btn-primary'
                    } flex items-center gap-2`}
                  >
                    {mission.is_completed ? (
                      <>
                        <RefreshCw className="w-4 h-4" />
                        Repetir
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4" />
                        Iniciar
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">🏆 Logros</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {achievements?.map((achievement) => (
            <div
              key={achievement.key}
              className={`card ${
                achievement.is_unlocked
                  ? 'bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 border border-yellow-200 dark:border-yellow-800'
                  : 'opacity-50'
              }`}
            >
              <div className="text-center">
                <div className="text-4xl mb-2">{achievement.emoji}</div>
                <h3 className="font-bold text-gray-900 dark:text-white">{achievement.name}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{achievement.description}</p>
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
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">🔧 Tecnologías Desbloqueadas</h2>
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

      {/* Quiz Modal */}
      {selectedMission && (
        <QuizModal
          mission={selectedMission}
          onClose={() => setSelectedMission(null)}
          onSubmit={async (answers) => {
            const result = await completeMissionMutation.mutateAsync({
              missionId: selectedMission.id,
              answers,
            })
            return result
          }}
        />
      )}
    </div>
  )
}
