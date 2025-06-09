export interface User {
    id: string;
    email: string;
    fullName: string;
    isActive: boolean;
    isSuperuser: boolean;
    createdAt: string;
    updatedAt: string;
}

export interface Medicine {
    id: string;
    name: string;
    category: string;
    manufacturer: string;
    description: string;
    price: number;
    stock: number;
    requiresPrescription: boolean;
    createdAt: string;
    updatedAt: string;
}

export interface OrderItem {
    medicineId: string;
    quantity: number;
    unitPrice: number;
    subtotal: number;
    medicine?: Medicine;
}

export enum OrderStatus {
    PENDING = "pending",
    PROCESSING = "processing",
    COMPLETED = "completed",
    CANCELLED = "cancelled"
}

export interface Order {
    id: string;
    userId: string;
    status: OrderStatus;
    items: OrderItem[];
    totalAmount: number;
    createdAt: string;
    updatedAt: string;
}

export enum PrescriptionStatus {
    ACTIVE = "active",
    EXPIRED = "expired",
    FULFILLED = "fulfilled"
}

export interface Prescription {
    id: string;
    userId: string;
    doctorName: string;
    status: PrescriptionStatus;
    medicines: Medicine[];
    createdAt: string;
    updatedAt: string;
}

export interface SearchFilters {
    name?: string;
    category?: string;
    minPrice?: number;
    maxPrice?: number;
    inStock?: boolean;
    requiresPrescription?: boolean;
    skip?: number;
    limit?: number;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
}

export interface ApiError {
    statusCode: number;
    message: string;
    details?: Record<string, any>;
} 