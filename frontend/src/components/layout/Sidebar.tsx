import { Link, useLocation } from 'react-router-dom'
import { Home, BookOpen, Gamepad2, User, Settings, ChevronRight } from 'lucide-react'
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
    { icon: Settings, label: 'Ajustes', path: '/settings' },
  ]

  return (
    <aside className="w-56 flex-shrink-0 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 min-h-[calc(100vh-64px)] sticky top-16">
      <nav className="p-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path ||
            (item.path === '/modules' && location.pathname.startsWith('/modules'))
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-primary text-white shadow-sm shadow-primary/25'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'
              )}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {modules && modules.length > 0 && (
        <div className="px-3 py-4 border-t border-gray-100 dark:border-gray-800">
          <h3 className="px-3 mb-2 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
            Progreso
          </h3>
          <div className="space-y-0.5">
            {modules.slice(0, 6).map((module) => {
              const isActive = location.pathname.includes(module.id)
              return (
                <Link
                  key={module.id}
                  to={`/modules/${module.id}`}
                  className={cn(
                    'group flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-all duration-200',
                    isActive
                      ? 'bg-primary/10 text-primary dark:text-primary-400'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
                  )}
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="text-sm">
                      {module.status === 'completed' && '✓'}
                      {module.status === 'in_progress' && '▸'}
                      {module.status === 'locked' && '○'}
                    </span>
                    <span className="truncate font-medium">M{module.number}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <div className="w-12 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className={cn(
                          'h-full rounded-full transition-all',
                          module.status === 'completed' ? 'bg-green-500' : 'bg-primary'
                        )}
                        style={{ width: `${module.progress_percentage}%` }}
                      />
                    </div>
                    <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                </Link>
              )
            })}
          </div>
        </div>
      )}

      {/* Pro upgrade banner */}
      <div className="absolute bottom-0 left-0 right-0 p-3">
        <div className="bg-gradient-to-r from-primary/10 to-secondary/10 dark:from-primary/20 dark:to-secondary/20 rounded-lg p-3 border border-primary/20">
          <p className="text-[10px] font-bold text-primary dark:text-primary-400 uppercase tracking-wide mb-1">Pro</p>
          <p className="text-xs text-gray-600 dark:text-gray-400">Acceso completo al contenido</p>
        </div>
      </div>
    </aside>
  )
}
