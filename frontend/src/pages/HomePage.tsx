import { Link } from 'react-router-dom'
import { BookOpen, Gamepad2, TrendingUp, Target } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { gameApi, progressApi } from '@/services/api'

export default function HomePage() {
  const { data: gameState } = useQuery({
    queryKey: ['gameState'],
    queryFn: gameApi.getGameState,
  })

  const { data: progress } = useQuery({
    queryKey: ['progress'],
    queryFn: progressApi.getProgress,
  })

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
          🚀 Bienvenido al Master en Data Engineering
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Aprende Data Engineering de forma práctica, con proyectos reales y un sistema
          de gamificación que te mantiene motivado
        </p>
      </div>

      {/* Main Cards */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Course Card */}
        <div className="card hover:shadow-lg dark:hover:shadow-gray-800 transition-shadow">
          <div className="flex items-center space-x-3 mb-4">
            <BookOpen className="w-8 h-8 text-primary" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">📚 Curso</h2>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-gray-600 dark:text-gray-400 mb-2">10 Módulos completos</p>
              <p className="text-3xl font-bold text-primary">
                {progress?.overall_percentage || 40}% Completado
              </p>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progress?.overall_percentage || 40}%` }}
              />
            </div>
            <Link to="/modules" className="btn btn-primary w-full block text-center">
              Continuar aprendiendo →
            </Link>
          </div>
        </div>

        {/* Game Card */}
        <div className="card hover:shadow-lg dark:hover:shadow-gray-800 transition-shadow bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20">
          <div className="flex items-center space-x-3 mb-4">
            <Gamepad2 className="w-8 h-8 text-primary" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">🎮 Juego</h2>
          </div>
          {gameState && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Nivel</p>
                  <p className="text-3xl font-bold text-primary">{gameState.level}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Rango</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-white">
                    {gameState.current_rank?.emoji} {gameState.current_rank?.name}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  XP: {gameState.xp} / {gameState.xp_for_next_level}
                </p>
                <div className="progress-bar">
                  <div
                    className="progress-fill bg-secondary"
                    style={{
                      width: `${(gameState.xp / (gameState.xp_for_next_level || 1)) * 100}%`,
                    }}
                  />
                </div>
              </div>
              <Link to="/game" className="btn btn-secondary w-full block text-center">
                Ir al juego →
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-4">
        <div className="card text-center">
          <TrendingUp className="w-8 h-8 text-primary mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {progress?.completed_modules || 4}/10
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">Módulos completados</p>
        </div>
        <div className="card text-center">
          <Target className="w-8 h-8 text-secondary mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {progress?.completed_topics || 13}/31
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">Temas completados</p>
        </div>
        <div className="card text-center">
          <Gamepad2 className="w-8 h-8 text-accent mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {gameState?.completed_missions?.length || 0}
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">Misiones completadas</p>
        </div>
        <div className="card text-center">
          <div className="text-2xl mb-2">🏆</div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {gameState?.unlocked_achievements?.length || 0}
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">Logros desbloqueados</p>
        </div>
      </div>

      {/* Next Steps */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">🎯 Siguiente paso</h3>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              Módulo 2 - Tema 2: SQL Intermedio
            </p>
            <p className="text-gray-600 dark:text-gray-400">JOINs, subconsultas, CTEs y funciones de ventana</p>
          </div>
          <Link to="/modules/modulo-02-sql" className="btn btn-primary">
            Continuar →
          </Link>
        </div>
      </div>
    </div>
  )
}
