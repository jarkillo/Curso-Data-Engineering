import { Check } from 'lucide-react'
import { cn } from '@/utils/cn'

interface Step {
  id: number
  title: string
}

interface ContentStepperProps {
  steps: Step[]
  currentStep: number
  completedSteps: number[]
  onStepClick: (step: number) => void
}

export default function ContentStepper({
  steps,
  currentStep,
  completedSteps,
  onStepClick,
}: ContentStepperProps) {
  return (
    <div className="mb-8">
      {/* Mobile: Compact version */}
      <div className="sm:hidden flex items-center justify-between bg-gray-50 dark:bg-gray-800/50 rounded-lg p-3">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Sección {currentStep + 1} de {steps.length}
        </span>
        <div className="flex gap-1">
          {steps.map((step, index) => (
            <button
              key={step.id}
              onClick={() => onStepClick(index)}
              className={cn(
                'w-2.5 h-2.5 rounded-full transition-all',
                index === currentStep
                  ? 'bg-primary w-6'
                  : completedSteps.includes(index)
                  ? 'bg-green-500'
                  : 'bg-gray-300 dark:bg-gray-600'
              )}
              aria-label={`Ir a sección ${index + 1}`}
            />
          ))}
        </div>
      </div>

      {/* Desktop: Full stepper */}
      <div className="hidden sm:block">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => {
            const isCompleted = completedSteps.includes(index)
            const isCurrent = index === currentStep
            const isClickable = isCompleted || index <= Math.max(...completedSteps, 0) + 1

            return (
              <div key={step.id} className="flex items-center flex-1 last:flex-none">
                {/* Step circle */}
                <button
                  onClick={() => isClickable && onStepClick(index)}
                  disabled={!isClickable}
                  className={cn(
                    'flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all font-medium text-sm',
                    isCurrent
                      ? 'border-primary bg-primary text-white shadow-md shadow-primary/25'
                      : isCompleted
                      ? 'border-green-500 bg-green-500 text-white cursor-pointer hover:shadow-md'
                      : isClickable
                      ? 'border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 cursor-pointer hover:border-primary hover:text-primary'
                      : 'border-gray-200 dark:border-gray-700 text-gray-300 dark:text-gray-600 cursor-not-allowed'
                  )}
                  aria-label={`Sección ${index + 1}: ${step.title}`}
                >
                  {isCompleted ? (
                    <Check className="w-5 h-5" />
                  ) : (
                    index + 1
                  )}
                </button>

                {/* Connector line */}
                {index < steps.length - 1 && (
                  <div
                    className={cn(
                      'flex-1 h-1 mx-3 rounded-full transition-all',
                      isCompleted
                        ? 'bg-green-500'
                        : 'bg-gray-200 dark:bg-gray-700'
                    )}
                  />
                )}
              </div>
            )
          })}
        </div>

        {/* Step titles */}
        <div className="flex items-start justify-between mt-3">
          {steps.map((step, index) => {
            const isCurrent = index === currentStep
            return (
              <div
                key={step.id}
                className={cn(
                  'flex-1 last:flex-none text-center px-1',
                  index === steps.length - 1 ? 'text-right' : index === 0 ? 'text-left' : ''
                )}
              >
                <span
                  className={cn(
                    'text-xs font-medium line-clamp-2',
                    isCurrent
                      ? 'text-primary'
                      : 'text-gray-500 dark:text-gray-400'
                  )}
                >
                  {step.title}
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
