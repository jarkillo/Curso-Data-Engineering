import { useState } from 'react'
import { useParams, useSearchParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { contentApi } from '@/services/api'
import { ChevronLeft } from 'lucide-react'

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
    { id: 'teoria', label: '📖 Teoría', icon: '📖' },
    { id: 'ejemplos', label: '💡 Ejemplos', icon: '💡' },
    { id: 'ejercicios', label: '✍️ Ejercicios', icon: '✍️' },
    { id: 'proyecto', label: '🛠️ Proyecto', icon: '🛠️' },
  ]

  return (
    <div className="max-w-5xl mx-auto">
      <Link
        to={`/modules/${moduleId}`}
        className="inline-flex items-center text-primary hover:text-primary-600 mb-4"
      >
        <ChevronLeft className="w-4 h-4" />
        Volver al módulo
      </Link>

      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 capitalize">
          {topicId?.replace(/-/g, ' ')}
        </h1>
      </div>

      {/* Section Tabs */}
      <div className="flex space-x-2 mb-6 border-b">
        {sections.map((s) => (
          <button
            key={s.id}
            onClick={() => setSearchParams({ section: s.id })}
            className={`px-4 py-2 font-medium transition-colors border-b-2 ${
              section === s.id
                ? 'text-primary border-primary'
                : 'text-gray-600 border-transparent hover:text-gray-900'
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="card">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
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
          <div className="text-center py-12">
            <p className="text-gray-600">Contenido no disponible</p>
          </div>
        )}
      </div>
    </div>
  )
}
