import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/router'

interface User {
  id: number
  email: string
  created_at: string
}

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  isAuthenticated: boolean
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isLoading: true,
    isAuthenticated: false,
  })
  const router = useRouter()

  useEffect(() => {
    const initAuth = () => {
      try {
        const token = localStorage.getItem('token')
        const userStr = localStorage.getItem('user')
        
        if (token && userStr) {
          const user = JSON.parse(userStr)
          setAuthState({
            user,
            token,
            isLoading: false,
            isAuthenticated: true,
          })
        } else {
          setAuthState({
            user: null,
            token: null,
            isLoading: false,
            isAuthenticated: false,
          })
        }
      } catch (error) {
        console.error('Auth initialization error:', error)
        setAuthState({
          user: null,
          token: null,
          isLoading: false,
          isAuthenticated: false,
        })
      }
    }

    initAuth()
  }, [])

  const login = useCallback((token: string, user: User) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    
    setAuthState({
      user,
      token,
      isLoading: false,
      isAuthenticated: true,
    })
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    
    setAuthState({
      user: null,
      token: null,
      isLoading: false,
      isAuthenticated: false,
    })
    
    router.push('/login')
  }, [router])

  const requireAuth = useCallback(() => {
    if (!authState.isLoading && !authState.isAuthenticated) {
      router.push('/login')
    }
  }, [authState.isLoading, authState.isAuthenticated, router])

  return {
    ...authState,
    login,
    logout,
    requireAuth,
  }
} 