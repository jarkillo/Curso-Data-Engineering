import { Link } from 'react-router-dom'
import { Gamepad2, LogOut, Moon, Sun, Sparkles } from 'lucide-react'
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
    <header className="h-16 bg-white dark:bg-gray-900 sticky top-0 z-50 border-b border-gray-200 dark:border-gray-800 transition-colors">
      <div className="h-full px-4 lg:px-6 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 bg-gradient-to-br from-primary to-primary-600 rounded-lg flex items-center justify-center shadow-sm shadow-primary/25 group-hover:shadow-md group-hover:shadow-primary/30 transition-shadow">
            <span className="text-white text-sm font-bold">DE</span>
          </div>
          <div className="hidden sm:block">
            <h1 className="text-base font-bold text-gray-900 dark:text-white leading-tight">
              Master Data Engineering
            </h1>
            <p className="text-[10px] text-gray-500 dark:text-gray-500 font-medium uppercase tracking-wide">
              con Inteligencia Artificial
            </p>
          </div>
        </Link>

        {/* Right Actions */}
        <div className="flex items-center gap-2">
          {/* Game Button */}
          <Link
            to="/game"
            className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-primary/10 to-secondary/10 dark:from-primary/20 dark:to-secondary/20 text-primary dark:text-primary-400 rounded-lg hover:from-primary/20 hover:to-secondary/20 dark:hover:from-primary/30 dark:hover:to-secondary/30 transition-all border border-primary/10"
          >
            <Gamepad2 className="w-4 h-4" />
            <span className="text-sm font-semibold hidden sm:inline">Juego</span>
            {gameState && (
              <span className="px-1.5 py-0.5 bg-primary text-white rounded text-[10px] font-bold">
                {gameState.level}
              </span>
            )}
          </Link>

          {/* Theme Toggle */}
          <button
            onClick={toggleDarkMode}
            className="w-9 h-9 flex items-center justify-center text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            title={isDarkMode ? 'Modo claro' : 'Modo oscuro'}
          >
            {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* User Menu */}
          <div className="flex items-center gap-2 pl-2 border-l border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg">
              <div className="w-7 h-7 bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-600 rounded-full flex items-center justify-center">
                <span className="text-xs font-bold text-gray-600 dark:text-gray-300 uppercase">
                  {user?.username?.[0] || 'U'}
                </span>
              </div>
              <div className="hidden md:block">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 leading-tight">
                  {user?.username || 'Usuario'}
                </p>
                {user?.tier === 'pro' ? (
                  <span className="inline-flex items-center gap-0.5 text-[10px] font-bold text-amber-600 dark:text-amber-400">
                    <Sparkles className="w-2.5 h-2.5" /> PRO
                  </span>
                ) : (
                  <span className="text-[10px] text-gray-500 dark:text-gray-500">Plan Gratis</span>
                )}
              </div>
            </div>

            <button
              onClick={logout}
              className="w-9 h-9 flex items-center justify-center text-gray-400 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
              title="Cerrar sesión"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
