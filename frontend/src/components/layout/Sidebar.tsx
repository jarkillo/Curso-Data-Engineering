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
    <aside className="w-64 flex-shrink-0 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 min-h-[calc(100vh-64px)] sticky top-16 overflow-y-auto">
      <nav className="p-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path ||
            (item.path === '/modules' && location.pathname.startsWith('/modules'))
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-white'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
              )}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {modules && modules.length > 0 && (
        <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-800">
          <h3 className="px-4 mb-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
            Módulos
          </h3>
          <div className="space-y-1">
            {modules.slice(0, 6).map((module) => {
              const isActive = location.pathname.includes(module.id)
              return (
                <Link
                  key={module.id}
                  to={`/modules/${module.id}`}
                  className={cn(
                    'flex items-center justify-between px-4 py-2.5 rounded-lg text-sm transition-colors',
                    isActive
                      ? 'bg-primary/10 text-primary dark:text-primary-400'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                  )}
                >
                  <div className="flex items-center gap-2">
                    <span>
                      {module.status === 'completed' && '✅'}
                      {module.status === 'in_progress' && '▶️'}
                      {module.status === 'locked' && '🔒'}
                    </span>
                    <span className="font-medium">Módulo {module.number}</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-500">
                    {module.progress_percentage}%
                  </span>
                </Link>
              )
            })}
          </div>
        </div>
      )}
    </aside>
  )
}
