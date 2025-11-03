import { Link } from 'react-router-dom'
import { Gamepad2, User, LogOut } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { gameApi } from '@/services/api'
import { useAuth } from '@/context/AuthContext'

export default function Header() {
  const { user, logout } = useAuth()
  const { data: gameState } = useQuery({
    queryKey: ['gameState'],
    queryFn: gameApi.getGameState,
  })

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">DE</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Master Data Engineering</h1>
              <p className="text-xs text-gray-500">con Inteligencia Artificial</p>
            </div>
          </Link>

          <div className="flex items-center space-x-4">
            <Link
              to="/game"
              className="flex items-center space-x-2 px-4 py-2 bg-primary-50 text-primary rounded-lg hover:bg-primary-100 transition-colors"
            >
              <Gamepad2 className="w-5 h-5" />
              <span className="font-medium">Juego</span>
              {gameState && (
                <span className="ml-2 px-2 py-0.5 bg-primary text-white rounded-full text-xs">
                  Nivel {gameState.level}
                </span>
              )}
            </Link>

            <div className="flex items-center space-x-2 px-4 py-2 bg-gray-50 rounded-lg">
              <User className="w-5 h-5 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
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
              className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
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
