import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { ref, computed } from 'vue';
import type {
    Medicine,
    Order,
    Prescription,
    User,
    SearchFilters,
    PaginatedResponse,
    ApiError
} from '@/types/models';

class ApiService {
    private api: AxiosInstance;
    private _isLoading = ref(false);
    private _error = ref<ApiError | null>(null);

    constructor() {
        this.api = axios.create({
            baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Add request interceptor
        this.api.interceptors.request.use(
            (config) => {
                this._isLoading.value = true;
                this._error.value = null;

                const token = localStorage.getItem('token');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }

                return config;
            },
            (error) => {
                this._isLoading.value = false;
                return Promise.reject(error);
            }
        );

        // Add response interceptor
        this.api.interceptors.response.use(
            (response) => {
                this._isLoading.value = false;
                return response;
            },
            (error: AxiosError) => {
                this._isLoading.value = false;
                this._error.value = {
                    statusCode: error.response?.status || 500,
                    message: error.response?.data?.message || 'An unexpected error occurred',
                    details: error.response?.data?.details
                };
                return Promise.reject(error);
            }
        );
    }

    // Computed properties
    public get isLoading() {
        return computed(() => this._isLoading.value);
    }

    public get error() {
        return computed(() => this._error.value);
    }

    // Authentication
    async login(email: string, password: string): Promise<string> {
        const response = await this.api.post<{ access_token: string }>('/auth/login', {
            email,
            password
        });
        return response.data.access_token;
    }

    async getCurrentUser(): Promise<User> {
        const response = await this.api.get<User>('/users/me');
        return response.data;
    }

    // Medicines
    async searchMedicines(filters: SearchFilters): Promise<PaginatedResponse<Medicine>> {
        const response = await this.api.get<PaginatedResponse<Medicine>>('/medicines', {
            params: filters
        });
        return response.data;
    }

    async getMedicineById(id: string): Promise<Medicine> {
        const response = await this.api.get<Medicine>(`/medicines/${id}`);
        return response.data;
    }

    async getMedicineRecommendations(): Promise<Medicine[]> {
        const response = await this.api.get<Medicine[]>('/medicines/recommendations');
        return response.data;
    }

    // Orders
    async createOrder(items: { medicineId: string; quantity: number }[]): Promise<Order> {
        const response = await this.api.post<Order>('/orders', { items });
        return response.data;
    }

    async getUserOrders(): Promise<Order[]> {
        const response = await this.api.get<Order[]>('/orders/my-orders');
        return response.data;
    }

    async getOrderById(id: string): Promise<Order> {
        const response = await this.api.get<Order>(`/orders/${id}`);
        return response.data;
    }

    // Prescriptions
    async uploadPrescription(
        file: File,
        medicines: string[],
        doctorName: string
    ): Promise<Prescription> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('medicines', JSON.stringify(medicines));
        formData.append('doctorName', doctorName);

        const response = await this.api.post<Prescription>('/prescriptions', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    }

    async getUserPrescriptions(): Promise<Prescription[]> {
        const response = await this.api.get<Prescription[]>('/prescriptions/my-prescriptions');
        return response.data;
    }

    // Error handling helper
    private handleError(error: unknown): never {
        if (axios.isAxiosError(error)) {
            throw {
                statusCode: error.response?.status || 500,
                message: error.response?.data?.message || 'An unexpected error occurred',
                details: error.response?.data?.details
            };
        }
        throw error;
    }
}

// Create a singleton instance
export const apiService = new ApiService(); 