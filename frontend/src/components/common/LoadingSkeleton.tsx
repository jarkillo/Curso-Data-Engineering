export function CardSkeleton() {
  return (
    <div className="card animate-pulse">
      <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4 mb-4"></div>
      <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-1/2 mb-2"></div>
      <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-5/6"></div>
    </div>
  )
}

export function StatCardSkeleton() {
  return (
    <div className="card text-center animate-pulse">
      <div className="w-8 h-8 bg-gray-300 dark:bg-gray-600 rounded mx-auto mb-2"></div>
      <div className="h-6 bg-gray-300 dark:bg-gray-600 rounded w-16 mx-auto mb-2"></div>
      <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-24 mx-auto"></div>
    </div>
  )
}

export function MissionCardSkeleton() {
  return (
    <div className="card animate-pulse">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded"></div>
            <div className="h-5 bg-gray-300 dark:bg-gray-600 rounded w-1/3"></div>
          </div>
          <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4 mb-3 ml-9"></div>
          <div className="flex items-center space-x-4 ml-9">
            <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-32"></div>
            <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-16"></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export function AchievementCardSkeleton() {
  return (
    <div className="card animate-pulse">
      <div className="text-center">
        <div className="w-16 h-16 bg-gray-300 dark:bg-gray-600 rounded-full mx-auto mb-2"></div>
        <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4 mx-auto mb-1"></div>
        <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-full mx-auto"></div>
      </div>
    </div>
  )
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center space-x-4 animate-pulse">
          <div className="w-8 h-8 bg-gray-300 dark:bg-gray-600 rounded"></div>
          <div className="flex-1 h-4 bg-gray-300 dark:bg-gray-600 rounded"></div>
          <div className="w-20 h-4 bg-gray-300 dark:bg-gray-600 rounded"></div>
        </div>
      ))}
    </div>
  )
}

export function ProgressBarSkeleton() {
  return (
    <div className="space-y-2 animate-pulse">
      <div className="flex justify-between text-sm">
        <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-24"></div>
        <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-12"></div>
      </div>
      <div className="progress-bar">
        <div className="h-full bg-gray-300 dark:bg-gray-600 w-2/3"></div>
      </div>
    </div>
  )
}

export function PageSkeleton() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center py-12 animate-pulse">
        <div className="h-12 bg-gray-300 dark:bg-gray-600 rounded w-2/3 mx-auto mb-4"></div>
        <div className="h-6 bg-gray-300 dark:bg-gray-600 rounded w-1/2 mx-auto"></div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <CardSkeleton />
        <CardSkeleton />
      </div>

      <div className="grid md:grid-cols-4 gap-4">
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
      </div>
    </div>
  )
}
