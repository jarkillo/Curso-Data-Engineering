import { useParams, useSearchParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { contentApi } from '@/services/api'
import { ChevronLeft, BookOpen, Lightbulb, PenTool, Wrench } from 'lucide-react'
import { cn } from '@/utils/cn'

export default function TopicPage() {
  const { moduleId, topicId } = useParams()
  const [searchParams, setSearchParams] = useSearchParams()
  const section = searchParams.get('section') || 'teoria'

  const { data: content, isLoading } = useQuery({
    queryKey: ['content', moduleId, topicId, section],
    queryFn: () => contentApi.getContent(moduleId!, topicId!, section),
    enabled: !!moduleId && !!topicId,
  })

  const sections = [
    { id: 'teoria', label: 'Teoría', icon: BookOpen },
    { id: 'ejemplos', label: 'Ejemplos', icon: Lightbulb },
    { id: 'ejercicios', label: 'Ejercicios', icon: PenTool },
    { id: 'proyecto', label: 'Proyecto', icon: Wrench },
  ]

  return (
    <div className="max-w-4xl">
      {/* Breadcrumb */}
      <Link
        to={`/modules/${moduleId}`}
        className="inline-flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400 hover:text-primary dark:hover:text-primary-400 transition-colors mb-4"
      >
        <ChevronLeft className="w-4 h-4" />
        <span>Volver al módulo</span>
      </Link>

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white capitalize leading-tight">
          {topicId?.replace(/-/g, ' ')}
        </h1>
      </div>

      {/* Section Tabs */}
      <div className="flex gap-1 p-1 mb-6 bg-gray-100 dark:bg-gray-800 rounded-lg w-fit">
        {sections.map((s) => {
          const Icon = s.icon
          const isActive = section === s.id
          return (
            <button
              key={s.id}
              onClick={() => setSearchParams({ section: s.id })}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all',
                isActive
                  ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              )}
            >
              <Icon className="w-4 h-4" />
              <span className="hidden sm:inline">{s.label}</span>
            </button>
          )
        })}
      </div>

      {/* Content */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="p-6 lg:p-8">
          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : content ? (
            <ReactMarkdown
              className="markdown-content"
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '')
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language={match[1]}
                      PreTag="div"
                      customStyle={{
                        margin: '1.5rem 0',
                        borderRadius: '0.5rem',
                        fontSize: '0.875rem',
                      }}
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                },
              }}
            >
              {content.content}
            </ReactMarkdown>
          ) : (
            <div className="text-center py-16">
              <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-8 h-8 text-gray-400" />
              </div>
              <p className="text-gray-600 dark:text-gray-400">Contenido no disponible</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
