import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import type { User, LoginRequest, RegisterRequest } from '../types/auth'
import { authApi } from '../services/api'
import { showToast } from '../components/common/Toast'

interface AuthContextType {
  user: User | null
  token: string | null
  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load token from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
      // Fetch user info
      authApi
        .getMe(storedToken)
        .then((userData) => {
          setUser(userData)
        })
        .catch(() => {
          // Invalid token
          localStorage.removeItem('token')
          setToken(null)
        })
        .finally(() => {
          setIsLoading(false)
        })
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (data: LoginRequest) => {
    try {
      const response = await authApi.login(data)
      setToken(response.access_token)
      localStorage.setItem('token', response.access_token)

      // Fetch user info
      const userData = await authApi.getMe(response.access_token)
      setUser(userData)
      showToast.success(`¡Bienvenido, ${userData.username}!`)
    } catch (error: any) {
      showToast.error(error.response?.data?.detail || 'Error al iniciar sesión')
      throw error
    }
  }

  const register = async (data: RegisterRequest) => {
    try {
      await authApi.register(data)
      // Auto-login after register
      await login({ email: data.email, password: data.password })
      showToast.success('¡Cuenta creada exitosamente!')
    } catch (error: any) {
      showToast.error(error.response?.data?.detail || 'Error al registrarse')
      throw error
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    showToast.info('Sesión cerrada')
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
