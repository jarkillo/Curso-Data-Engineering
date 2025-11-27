import { Link } from 'react-router-dom'
import { Gamepad2, User, LogOut, Moon, Sun } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { gameApi } from '@/services/api'
import { useAuth } from '@/context/AuthContext'
import { useThemeStore } from '@/store/themeStore'

export default function Header() {
  const { user, logout } = useAuth()
  const { isDarkMode, toggleDarkMode } = useThemeStore()
  const { data: gameState } = useQuery({
    queryKey: ['gameState'],
    queryFn: gameApi.getGameState,
  })

  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm sticky top-0 z-50 border-b border-gray-200 dark:border-gray-700 transition-colors">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">DE</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">Master Data Engineering</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">con Inteligencia Artificial</p>
            </div>
          </Link>

          <div className="flex items-center space-x-4">
            <Link
              to="/game"
              className="flex items-center space-x-2 px-4 py-2 bg-primary-50 dark:bg-primary-900/30 text-primary dark:text-primary-400 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors"
            >
              <Gamepad2 className="w-5 h-5" />
              <span className="font-medium">Juego</span>
              {gameState && (
                <span className="ml-2 px-2 py-0.5 bg-primary text-white rounded-full text-xs">
                  Nivel {gameState.level}
                </span>
              )}
            </Link>

            <button
              onClick={toggleDarkMode}
              className="flex items-center justify-center p-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
              title={isDarkMode ? 'Modo claro' : 'Modo oscuro'}
            >
              {isDarkMode ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </button>

            <div className="flex items-center space-x-2 px-4 py-2 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <User className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {user?.username || 'Usuario'}
              </span>
              {user?.tier === 'pro' && (
                <span className="ml-2 px-2 py-0.5 bg-yellow-500 text-white rounded-full text-xs">
                  PRO
                </span>
              )}
            </div>

            <button
              onClick={logout}
              className="flex items-center space-x-2 px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors"
              title="Cerrar sesión"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
