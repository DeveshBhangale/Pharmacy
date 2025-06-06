import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/Home.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/Login.vue'),
            meta: { guest: true }
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/views/Register.vue'),
            meta: { guest: true }
        },
        {
            path: '/medicines',
            name: 'medicines',
            component: () => import('@/views/Medicines.vue')
        },
        {
            path: '/medicines/:id',
            name: 'medicine-details',
            component: () => import('@/views/MedicineDetails.vue')
        },
        {
            path: '/prescriptions',
            name: 'prescriptions',
            component: () => import('@/views/Prescriptions.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/prescriptions/upload',
            name: 'upload-prescription',
            component: () => import('@/views/UploadPrescription.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/orders',
            name: 'orders',
            component: () => import('@/views/Orders.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('@/views/Profile.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('@/views/NotFound.vue')
        }
    ]
})

// Navigation guards
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const isGuestOnly = to.matched.some(record => record.meta.guest)

    if (requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } })
    } else if (isGuestOnly && authStore.isAuthenticated) {
        next({ name: 'home' })
    } else {
        next()
    }
})

export default router 