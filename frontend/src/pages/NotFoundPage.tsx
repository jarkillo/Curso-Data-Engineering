import { Link } from 'react-router-dom'
import { Home } from 'lucide-react'

export default function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <h1 className="text-9xl font-bold text-primary mb-4">404</h1>
      <h2 className="text-3xl font-bold text-gray-900 mb-2">Página no encontrada</h2>
      <p className="text-gray-600 mb-8">
        Lo sentimos, la página que buscas no existe.
      </p>
      <Link to="/" className="btn btn-primary inline-flex items-center space-x-2">
        <Home className="w-5 h-5" />
        <span>Volver al inicio</span>
      </Link>
    </div>
  )
}
