import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { ChevronRight, Lock, CheckCircle, PlayCircle } from 'lucide-react'
import { contentApi } from '@/services/api'

export default function ModulesPage() {
  const { moduleId } = useParams()

  const { data: modules } = useQuery({
    queryKey: ['modules'],
    queryFn: contentApi.getModules,
  })

  const { data: selectedModule } = useQuery({
    queryKey: ['module', moduleId],
    queryFn: () => contentApi.getModule(moduleId!),
    enabled: !!moduleId,
  })

  if (moduleId && selectedModule) {
    return (
      <div className="max-w-4xl mx-auto">
        <Link to="/modules" className="text-primary hover:text-primary-600 mb-4 inline-block">
          ← Volver a módulos
        </Link>

        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Módulo {selectedModule.number}: {selectedModule.title}
          </h1>
          <div className="flex items-center space-x-4 mt-4">
            <span className={`badge ${
              selectedModule.status === 'completed' ? 'badge-success' :
              selectedModule.status === 'in_progress' ? 'badge-warning' :
              'badge-info'
            }`}>
              {selectedModule.status === 'completed' && '✅ Completado'}
              {selectedModule.status === 'in_progress' && '▶️ En progreso'}
              {selectedModule.status === 'locked' && '🔒 Bloqueado'}
            </span>
            <span className="text-gray-600 dark:text-gray-400">
              {selectedModule.progress_percentage}% completado
            </span>
          </div>
        </div>

        <div className="space-y-4">
          {selectedModule.topics.map((topic) => (
            <div key={topic.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    {topic.completed ? (
                      <CheckCircle className="w-6 h-6 text-green-500" />
                    ) : (
                      <PlayCircle className="w-6 h-6 text-primary" />
                    )}
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                      Tema {topic.number}: {topic.title}
                    </h3>
                  </div>
                  {topic.coverage && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 ml-9">
                      Cobertura de tests: {topic.coverage}%
                    </p>
                  )}
                  <div className="flex flex-wrap gap-2 mt-3 ml-9">
                    {topic.available_sections.map((section) => (
                      <Link
                        key={section}
                        to={`/modules/${moduleId}/${topic.id}?section=${section}`}
                        className="px-3 py-1 bg-primary-50 dark:bg-primary-900/30 text-primary dark:text-primary-300 rounded-lg text-sm hover:bg-primary-100 dark:hover:bg-primary-800/40 transition-colors"
                      >
                        {section === 'teoria' && '📖 Teoría'}
                        {section === 'ejemplos' && '💡 Ejemplos'}
                        {section === 'ejercicios' && '✍️ Ejercicios'}
                        {section === 'proyecto' && '🛠️ Proyecto'}
                      </Link>
                    ))}
                  </div>
                </div>
                <ChevronRight className="w-6 h-6 text-gray-400" />
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">📚 Módulos del Curso</h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          10 módulos completos para convertirte en Data Engineer profesional
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {modules?.map((module) => (
          <Link
            key={module.id}
            to={`/modules/${module.id}`}
            className="card hover:shadow-xl transition-all group"
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white group-hover:text-primary transition-colors">
                  Módulo {module.number}
                </h3>
                <p className="text-lg text-gray-700 dark:text-gray-300 mt-1">{module.title}</p>
              </div>
              {module.status === 'completed' && <CheckCircle className="w-8 h-8 text-green-500" />}
              {module.status === 'in_progress' && <PlayCircle className="w-8 h-8 text-primary" />}
              {module.status === 'locked' && <Lock className="w-8 h-8 text-gray-400" />}
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
                <span>{module.topic_count} temas</span>
                <span>{module.progress_percentage}% completado</span>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${module.progress_percentage}%` }}
                />
              </div>
            </div>

            <div className="mt-4">
              <span className={`badge ${
                module.status === 'completed' ? 'badge-success' :
                module.status === 'in_progress' ? 'badge-warning' :
                'badge-info'
              }`}>
                {module.status === 'completed' && '✅ Completado'}
                {module.status === 'in_progress' && '▶️ En progreso'}
                {module.status === 'locked' && '🔒 Bloqueado'}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
