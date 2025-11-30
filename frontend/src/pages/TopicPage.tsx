import React, { useState, useEffect, useMemo, useCallback } from 'react'
import { useParams, useSearchParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { contentApi } from '@/services/api'
import { ChevronLeft, ChevronRight, BookOpen, Lightbulb, PenTool, Wrench, CheckCircle } from 'lucide-react'
import { cn } from '@/utils/cn'
import ContentStepper from '@/components/content/ContentStepper'

// Split markdown content by h2 headers
function splitContentByHeaders(content: string): { title: string; content: string }[] {
  if (!content) return []

  // Split by ## headers (h2)
  const sections = content.split(/(?=^## )/gm)

  return sections
    .map((section, index) => {
      const lines = section.trim().split('\n')
      const firstLine = lines[0] || ''

      // Extract title from ## header or use default
      let title = `Sección ${index + 1}`
      if (firstLine.startsWith('## ')) {
        title = firstLine.replace(/^## /, '').trim()
      } else if (firstLine.startsWith('# ') && index === 0) {
        title = 'Introducción'
      }

      return {
        title,
        content: section.trim(),
      }
    })
    .filter((section) => section.content.length > 0)
}

// Get storage key for progress
function getProgressKey(moduleId: string, topicId: string, section: string): string {
  return `content-progress-${moduleId}-${topicId}-${section}`
}

export default function TopicPage() {
  const { moduleId, topicId } = useParams()
  const [searchParams, setSearchParams] = useSearchParams()
  const section = searchParams.get('section') || 'teoria'

  const [currentPage, setCurrentPage] = useState(0)
  const [completedPages, setCompletedPages] = useState<number[]>([])

  const { data: content, isLoading } = useQuery({
    queryKey: ['content', moduleId, topicId, section],
    queryFn: () => contentApi.getContent(moduleId!, topicId!, section),
    enabled: !!moduleId && !!topicId,
  })

  // Split content into pages
  const pages = useMemo(() => {
    if (!content?.content) return []
    const sections = splitContentByHeaders(content.content)
    // If only 1 section or content is short, return as single page
    if (sections.length <= 1 || content.content.length < 1500) {
      return [{ title: 'Contenido', content: content.content }]
    }
    return sections
  }, [content?.content])

  // Load progress from localStorage
  useEffect(() => {
    if (moduleId && topicId) {
      const key = getProgressKey(moduleId, topicId, section)
      const saved = localStorage.getItem(key)
      if (saved) {
        try {
          const parsed = JSON.parse(saved)
          setCompletedPages(parsed.completedPages || [])
          // Don't restore page, always start at beginning for fresh context
        } catch {
          setCompletedPages([])
        }
      } else {
        setCompletedPages([])
      }
      setCurrentPage(0)
    }
  }, [moduleId, topicId, section])

  // Save progress to localStorage
  useEffect(() => {
    if (moduleId && topicId && completedPages.length > 0) {
      const key = getProgressKey(moduleId, topicId, section)
      localStorage.setItem(key, JSON.stringify({ completedPages }))
    }
  }, [moduleId, topicId, section, completedPages])

  // Mark current page as completed when navigating away
  const markAsCompleted = useCallback((pageIndex: number) => {
    setCompletedPages((prev) => {
      if (prev.includes(pageIndex)) return prev
      return [...prev, pageIndex]
    })
  }, [])

  const goToPage = useCallback((page: number) => {
    if (page >= 0 && page < pages.length) {
      // Mark current page as completed before leaving
      markAsCompleted(currentPage)
      setCurrentPage(page)
      // Scroll to top of content
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }, [pages.length, currentPage, markAsCompleted])

  const goNext = useCallback(() => {
    goToPage(currentPage + 1)
  }, [currentPage, goToPage])

  const goPrev = useCallback(() => {
    goToPage(currentPage - 1)
  }, [currentPage, goToPage])

  // Mark last page as completed when finishing
  const finishSection = useCallback(() => {
    markAsCompleted(currentPage)
  }, [currentPage, markAsCompleted])

  const sections = [
    { id: 'teoria', label: 'Teoría', icon: BookOpen },
    { id: 'ejemplos', label: 'Ejemplos', icon: Lightbulb },
    { id: 'ejercicios', label: 'Ejercicios', icon: PenTool },
    { id: 'proyecto', label: 'Proyecto', icon: Wrench },
  ]

  const currentContent = pages[currentPage]?.content || ''
  const isLastPage = currentPage === pages.length - 1
  const isFirstPage = currentPage === 0
  const allCompleted = pages.length > 0 && completedPages.length >= pages.length

  // Calculate progress percentage
  const progressPercentage = pages.length > 0
    ? Math.round((completedPages.length / pages.length) * 100)
    : 0

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
        {pages.length > 1 && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {progressPercentage}% completado • {completedPages.length} de {pages.length} secciones
          </p>
        )}
      </div>

      {/* Section Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-200 dark:border-gray-700">
        {sections.map((s) => {
          const Icon = s.icon
          const isActive = section === s.id
          return (
            <button
              key={s.id}
              onClick={() => setSearchParams({ section: s.id })}
              className={cn(
                'flex items-center gap-2 px-4 py-3 text-sm font-medium transition-all border-b-2 -mb-px',
                isActive
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
              )}
            >
              <Icon className="w-4 h-4" />
              <span>{s.label}</span>
            </button>
          )
        })}
      </div>

      {/* Stepper (only show if multiple pages) */}
      {pages.length > 1 && !isLoading && (
        <ContentStepper
          steps={pages.map((p, i) => ({ id: i, title: p.title }))}
          currentStep={currentPage}
          completedSteps={completedPages}
          onStepClick={goToPage}
        />
      )}

      {/* Content */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="p-6 lg:p-8">
          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : currentContent ? (
            <>
              <ReactMarkdown
                className="markdown-content"
                remarkPlugins={[remarkGfm]}
                components={{
                  code(props) {
                    const { children, className, ...rest } = props
                    const match = /language-(\w+)/.exec(className || '')
                    const isInline = !match && !String(children).includes('\n')
                    return !isInline && match ? (
                      <SyntaxHighlighter
                        style={vscDarkPlus as Record<string, React.CSSProperties>}
                        language={match[1]}
                        PreTag="div"
                        customStyle={{
                          margin: '1.5rem 0',
                          borderRadius: '0.5rem',
                          fontSize: '0.875rem',
                        }}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...rest}>
                        {children}
                      </code>
                    )
                  },
                }}
              >
                {currentContent}
              </ReactMarkdown>

              {/* Navigation */}
              {pages.length > 1 && (
                <div className="mt-10 pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between">
                    {/* Previous button */}
                    <button
                      onClick={goPrev}
                      disabled={isFirstPage}
                      className={cn(
                        'flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-all',
                        isFirstPage
                          ? 'text-gray-300 dark:text-gray-600 cursor-not-allowed'
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                      )}
                    >
                      <ChevronLeft className="w-5 h-5" />
                      <span>Anterior</span>
                    </button>

                    {/* Page indicator */}
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {currentPage + 1} / {pages.length}
                    </span>

                    {/* Next / Complete button */}
                    {isLastPage ? (
                      <button
                        onClick={finishSection}
                        className={cn(
                          'flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium transition-all',
                          allCompleted
                            ? 'bg-green-500 text-white'
                            : 'bg-primary text-white hover:bg-primary-600'
                        )}
                      >
                        <CheckCircle className="w-5 h-5" />
                        <span>{allCompleted ? '¡Completado!' : 'Finalizar'}</span>
                      </button>
                    ) : (
                      <button
                        onClick={goNext}
                        className="flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-600 transition-all"
                      >
                        <span>Siguiente</span>
                        <ChevronRight className="w-5 h-5" />
                      </button>
                    )}
                  </div>
                </div>
              )}
            </>
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
