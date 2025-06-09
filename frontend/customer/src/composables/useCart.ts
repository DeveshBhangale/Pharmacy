import { ref, computed, watch } from 'vue';
import type { Medicine } from '@/types/models';

interface CartItem {
    medicine: Medicine;
    quantity: number;
}

export function useCart() {
    const items = ref<CartItem[]>([]);

    // Computed properties
    const totalItems = computed(() => {
        return items.value.reduce((total, item) => total + item.quantity, 0);
    });

    const totalAmount = computed(() => {
        return items.value.reduce((total, item) => {
            return total + (item.medicine.price * item.quantity);
        }, 0);
    });

    const isEmpty = computed(() => items.value.length === 0);

    // Methods
    function addItem(medicine: Medicine, quantity: number = 1) {
        const existingItem = items.value.find(item => item.medicine.id === medicine.id);

        if (existingItem) {
            // Check stock availability
            const newQuantity = existingItem.quantity + quantity;
            if (newQuantity <= medicine.stock) {
                existingItem.quantity = newQuantity;
            } else {
                throw new Error('Insufficient stock');
            }
        } else {
            // Check stock availability
            if (quantity <= medicine.stock) {
                items.value.push({ medicine, quantity });
            } else {
                throw new Error('Insufficient stock');
            }
        }
    }

    function removeItem(medicineId: string) {
        const index = items.value.findIndex(item => item.medicine.id === medicineId);
        if (index !== -1) {
            items.value.splice(index, 1);
        }
    }

    function updateQuantity(medicineId: string, quantity: number) {
        const item = items.value.find(item => item.medicine.id === medicineId);
        if (item) {
            // Check stock availability
            if (quantity <= item.medicine.stock) {
                item.quantity = quantity;
            } else {
                throw new Error('Insufficient stock');
            }
        }
    }

    function clearCart() {
        items.value = [];
    }

    function getItemQuantity(medicineId: string): number {
        const item = items.value.find(item => item.medicine.id === medicineId);
        return item?.quantity || 0;
    }

    // Persistence
    function saveToLocalStorage() {
        localStorage.setItem('cart', JSON.stringify(items.value));
    }

    function loadFromLocalStorage() {
        const savedCart = localStorage.getItem('cart');
        if (savedCart) {
            items.value = JSON.parse(savedCart);
        }
    }

    // Load cart on initialization
    loadFromLocalStorage();

    // Auto-save cart changes
    watch(items, () => {
        saveToLocalStorage();
    }, { deep: true });

    return {
        // State
        items,

        // Computed
        totalItems,
        totalAmount,
        isEmpty,

        // Methods
        addItem,
        removeItem,
        updateQuantity,
        clearCart,
        getItemQuantity
    };
} 