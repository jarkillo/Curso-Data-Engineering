import { Link, useLocation } from 'react-router-dom'
import { Home, BookOpen, Gamepad2, User, Settings } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { contentApi } from '@/services/api'
import { cn } from '@/utils/cn'

export default function Sidebar() {
  const location = useLocation()
  const { data: modules } = useQuery({
    queryKey: ['modules'],
    queryFn: contentApi.getModules,
  })

  const navItems = [
    { icon: Home, label: 'Inicio', path: '/' },
    { icon: BookOpen, label: 'Módulos', path: '/modules' },
    { icon: Gamepad2, label: 'Juego', path: '/game' },
    { icon: User, label: 'Perfil', path: '/profile' },
    { icon: Settings, label: 'Configuración', path: '/settings' },
  ]

  return (
    <aside className="w-64 bg-white dark:bg-gray-900 shadow-sm h-screen sticky top-16 overflow-y-auto border-r border-gray-200 dark:border-gray-700 transition-colors">
      <nav className="p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
                isActive
                  ? 'bg-primary text-white'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'
              )}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {modules && modules.length > 0 && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-2">
            Módulos
          </h3>
          <div className="space-y-1">
            {modules.slice(0, 6).map((module) => (
              <Link
                key={module.id}
                to={`/modules/${module.id}`}
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 rounded transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="truncate">
                    {module.status === 'completed' && '✅ '}
                    {module.status === 'in_progress' && '▶️ '}
                    {module.status === 'locked' && '🔒 '}
                    Módulo {module.number}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {module.progress_percentage}%
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </aside>
  )
}
