import { useState } from 'react'
import { X, CheckCircle, XCircle, RefreshCw } from 'lucide-react'
import { cn } from '@/utils/cn'
import type { Mission, MissionResult } from '@/types/game'

interface QuizModalProps {
  mission: Mission
  onClose: () => void
  onSubmit: (answers: number[]) => Promise<MissionResult>
}

export default function QuizModal({ mission, onClose, onSubmit }: QuizModalProps) {
  const [answers, setAnswers] = useState<number[]>(
    new Array(mission.questions.length).fill(-1)
  )
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [result, setResult] = useState<MissionResult | null>(null)

  const handleAnswerSelect = (questionIndex: number, optionIndex: number) => {
    if (result) return // Don't allow changes after submission
    const newAnswers = [...answers]
    newAnswers[questionIndex] = optionIndex
    setAnswers(newAnswers)
  }

  const handleSubmit = async () => {
    if (answers.includes(-1)) return // Not all answered
    setIsSubmitting(true)
    try {
      const res = await onSubmit(answers)
      setResult(res)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleRetry = () => {
    setAnswers(new Array(mission.questions.length).fill(-1))
    setResult(null)
  }

  const allAnswered = !answers.includes(-1)

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              {mission.title}
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {mission.is_completed ? 'Repetir misión (sin XP)' : `+${mission.xp_reward} XP`}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Questions */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {mission.questions.map((question, qIndex) => (
            <div key={question.id} className="space-y-3">
              <p className="font-medium text-gray-900 dark:text-white">
                {qIndex + 1}. {question.question}
              </p>
              <div className="space-y-2">
                {question.options.map((option, oIndex) => {
                  const isSelected = answers[qIndex] === oIndex
                  const isCorrect = question.correct_index === oIndex
                  const showResult = result !== null

                  let optionClass = 'border-gray-200 dark:border-gray-600'
                  if (showResult) {
                    if (isCorrect) {
                      optionClass = 'border-green-500 bg-green-50 dark:bg-green-900/20'
                    } else if (isSelected && !isCorrect) {
                      optionClass = 'border-red-500 bg-red-50 dark:bg-red-900/20'
                    }
                  } else if (isSelected) {
                    optionClass = 'border-primary bg-primary/5'
                  }

                  return (
                    <button
                      key={oIndex}
                      onClick={() => handleAnswerSelect(qIndex, oIndex)}
                      disabled={result !== null}
                      className={cn(
                        'w-full text-left p-3 rounded-lg border-2 transition-all',
                        optionClass,
                        !result && !isSelected && 'hover:border-gray-300 dark:hover:border-gray-500'
                      )}
                    >
                      <div className="flex items-center justify-between">
                        <span className={cn(
                          'text-sm',
                          isSelected ? 'text-gray-900 dark:text-white font-medium' : 'text-gray-600 dark:text-gray-300'
                        )}>
                          {option}
                        </span>
                        {showResult && isCorrect && (
                          <CheckCircle className="w-5 h-5 text-green-500" />
                        )}
                        {showResult && isSelected && !isCorrect && (
                          <XCircle className="w-5 h-5 text-red-500" />
                        )}
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700">
          {result ? (
            <div className="space-y-4">
              <div className={cn(
                'p-4 rounded-lg text-center',
                result.success
                  ? 'bg-green-50 dark:bg-green-900/20'
                  : 'bg-red-50 dark:bg-red-900/20'
              )}>
                <p className={cn(
                  'font-medium',
                  result.success ? 'text-green-700 dark:text-green-400' : 'text-red-700 dark:text-red-400'
                )}>
                  {result.message}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {result.correct_answers} de {result.total_questions} respuestas correctas
                </p>
              </div>
              <div className="flex gap-3">
                {!result.success && (
                  <button
                    onClick={handleRetry}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                  >
                    <RefreshCw className="w-4 h-4" />
                    Reintentar
                  </button>
                )}
                <button
                  onClick={onClose}
                  className={cn(
                    'flex-1 px-4 py-2.5 rounded-lg font-medium transition-colors',
                    result.success
                      ? 'bg-green-500 text-white hover:bg-green-600'
                      : 'bg-primary text-white hover:bg-primary-600'
                  )}
                >
                  {result.success ? '¡Continuar!' : 'Cerrar'}
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!allAnswered || isSubmitting}
              className={cn(
                'w-full px-4 py-3 rounded-lg font-medium transition-all',
                allAnswered
                  ? 'bg-primary text-white hover:bg-primary-600'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
              )}
            >
              {isSubmitting ? 'Verificando...' : allAnswered ? 'Enviar respuestas' : 'Responde todas las preguntas'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
