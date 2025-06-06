import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'

interface User {
    id: number
    email: string
    name: string
    avatar?: string
}

interface LoginCredentials {
    email: string
    password: string
}

interface RegisterData extends LoginCredentials {
    name: string
}

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(localStorage.getItem('token'))

    const isAuthenticated = computed(() => !!token.value)

    const setAuth = (newToken: string, userData: User) => {
        token.value = newToken
        user.value = userData
        localStorage.setItem('token', newToken)
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
    }

    const clearAuth = () => {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
    }

    const login = async (credentials: LoginCredentials) => {
        try {
            const response = await axios.post('/api/v1/auth/login', credentials)
            const { access_token, user: userData } = response.data
            setAuth(access_token, userData)
            return userData
        } catch (error) {
            clearAuth()
            throw error
        }
    }

    const register = async (data: RegisterData) => {
        try {
            const response = await axios.post('/api/v1/auth/register', data)
            const { access_token, user: userData } = response.data
            setAuth(access_token, userData)
            return userData
        } catch (error) {
            clearAuth()
            throw error
        }
    }

    const logout = async () => {
        try {
            await axios.post('/api/v1/auth/logout')
        } finally {
            clearAuth()
        }
    }

    const fetchUser = async () => {
        try {
            const response = await axios.get('/api/v1/auth/me')
            user.value = response.data
            return user.value
        } catch (error) {
            clearAuth()
            throw error
        }
    }

    // Initialize auth state
    if (token.value) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        fetchUser().catch(() => {
            // If fetching user fails, clear auth state
            clearAuth()
        })
    }

    return {
        user,
        token,
        isAuthenticated,
        login,
        register,
        logout,
        fetchUser
    }
}) 