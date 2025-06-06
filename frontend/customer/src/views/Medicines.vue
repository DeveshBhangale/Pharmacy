<template>
  <div class="bg-gray-100 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-8 flex gap-8">
      <!-- Sidebar Filters -->
      <aside class="hidden lg:block w-64 bg-white rounded-lg shadow p-6 h-fit">
        <h2 class="text-lg font-bold mb-4 text-[#232f3e]">Filters</h2>
        <div class="mb-6">
          <h3 class="font-semibold mb-2">Categories</h3>
          <div class="space-y-1">
            <label v-for="category in categories" :key="category" class="flex items-center text-sm">
              <input type="checkbox" v-model="selectedCategories" :value="category" class="mr-2 accent-[#ff9900]" />
              {{ category }}
            </label>
          </div>
        </div>
        <div>
          <h3 class="font-semibold mb-2">Price Range</h3>
          <div class="flex items-center space-x-2">
            <input type="number" v-model.number="priceRange.min" class="w-16 px-2 py-1 border rounded text-sm" placeholder="Min" />
            <span>-</span>
            <input type="number" v-model.number="priceRange.max" class="w-16 px-2 py-1 border rounded text-sm" placeholder="Max" />
          </div>
        </div>
        <button @click="applyFilters" class="mt-6 w-full bg-[#ff9900] text-black font-bold py-2 rounded hover:bg-[#e47911] transition">Apply Filters</button>
      </aside>

      <!-- Product Grid -->
      <section class="flex-1">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
          <h1 class="text-2xl font-bold text-[#232f3e]">Medicines & Healthcare</h1>
          <div class="relative w-full sm:w-80">
            <input type="text" v-model="searchQuery" placeholder="Search medicines..." class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#ff9900]" />
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z"/></svg>
          </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          <div v-for="product in filteredProducts" :key="product.id" class="bg-white rounded-lg shadow hover:shadow-xl transition p-4 flex flex-col group cursor-pointer">
            <img :src="product.image" :alt="product.name" class="h-40 w-full object-contain mb-4 rounded" />
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-[#232f3e] mb-1 group-hover:text-[#ff9900] transition">{{ product.name }}</h3>
              <p class="text-sm text-gray-500 mb-2">{{ product.category }}</p>
              <div class="flex items-center mb-2">
                <span class="text-[#ff9900] font-bold mr-2">₹{{ product.price }}</span>
                <span class="flex items-center text-xs text-yellow-400">
                  <svg v-for="n in 5" :key="n" :class="{'text-yellow-400': n <= Math.round(product.rating), 'text-gray-300': n > Math.round(product.rating)}" class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.967a1 1 0 00.95.69h4.175c.969 0 1.371 1.24.588 1.81l-3.38 2.455a1 1 0 00-.364 1.118l1.287 3.966c.3.922-.755 1.688-1.54 1.118l-3.38-2.455a1 1 0 00-1.175 0l-3.38 2.455c-.784.57-1.838-.196-1.54-1.118l1.287-3.966a1 1 0 00-.364-1.118L2.04 9.394c-.783-.57-.38-1.81.588-1.81h4.175a1 1 0 00.95-.69l1.286-3.967z"/></svg>
                </span>
              </div>
            </div>
            <router-link :to="'/medicines/' + product.id" class="mt-2 bg-[#ff9900] text-black font-bold py-2 rounded hover:bg-[#e47911] text-center transition">View Details</router-link>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedCategories = ref<string[]>([])
const priceRange = ref({ min: 0, max: 10000 })

const categories = [
  'Medicines',
  'Supplements',
  'Personal Care',
  'Medical Devices',
  'First Aid',
  'Health Food'
]

const products = ref([
  {
    id: 1,
    name: 'Vitamin D3 1000 IU',
    category: 'Supplements',
    price: 499,
    rating: 4.5,
    image: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    id: 2,
    name: 'Digital BP Monitor',
    category: 'Medical Devices',
    price: 2499,
    rating: 4.7,
    image: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    id: 3,
    name: 'Face Wash',
    category: 'Personal Care',
    price: 299,
    rating: 4.2,
    image: 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    id: 4,
    name: 'Protein Powder',
    category: 'Supplements',
    price: 1999,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1577174881658-0f30ed549adc?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    id: 5,
    name: 'First Aid Kit',
    category: 'First Aid',
    price: 799,
    rating: 4.3,
    image: 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    id: 6,
    name: 'Organic Honey',
    category: 'Health Food',
    price: 599,
    rating: 4.6,
    image: 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
])

const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategories.value.length === 0 || selectedCategories.value.includes(product.category)
    const matchesPrice = product.price >= priceRange.value.min && product.price <= priceRange.value.max
    return matchesSearch && matchesCategory && matchesPrice
  })
})

const applyFilters = () => {
  // Filters are automatically applied through the computed property
}
</script> 