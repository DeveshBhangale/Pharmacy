<template>
  <div class="bg-gray-100 min-h-screen py-8">
    <div v-if="loading" class="max-w-6xl mx-auto bg-white rounded-lg shadow p-8 flex items-center justify-center text-lg text-gray-500">
      Loading product details...
    </div>
    <div v-else-if="error" class="max-w-6xl mx-auto bg-white rounded-lg shadow p-8 flex items-center justify-center text-lg text-red-500">
      {{ error }}
    </div>
    <div v-else-if="product" class="max-w-6xl mx-auto bg-white rounded-lg shadow p-8 flex flex-col md:flex-row gap-10">
      <!-- Product Image -->
      <div class="flex-shrink-0 flex justify-center items-center md:w-1/2">
        <img :src="product.image_url || placeholderImg" :alt="product.name" class="w-80 h-80 object-contain rounded border border-gray-200 bg-gray-50" />
      </div>
      <!-- Product Info -->
      <div class="flex-1 flex flex-col justify-between">
        <div>
          <h1 class="text-3xl font-bold text-[#232f3e] mb-2">{{ product.name }}</h1>
          <div class="flex items-center mb-4">
            <span class="flex items-center text-yellow-400 mr-2">
              <svg v-for="n in 5" :key="n" :class="{'text-yellow-400': n <= Math.round(product.rating || 4.5), 'text-gray-300': n > Math.round(product.rating || 4.5)}" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.967a1 1 0 00.95.69h4.175c.969 0 1.371 1.24.588 1.81l-3.38 2.455a1 1 0 00-.364 1.118l1.287 3.966c.3.922-.755 1.688-1.54 1.118l-3.38-2.455a1 1 0 00-1.175 0l-3.38 2.455c-.784.57-1.838-.196-1.54-1.118l1.287-3.966a1 1 0 00-.364-1.118L2.04 9.394c-.783-.57-.38-1.81.588-1.81h4.175a1 1 0 00.95-.69l1.286-3.967z"/></svg>
            </span>
            <span class="text-sm text-gray-500">{{ product.rating || 4.5 }} ({{ product.reviews || 128 }} reviews)</span>
          </div>
          <div class="text-2xl font-bold text-[#ff9900] mb-2">₹{{ product.price }}</div>
          <div class="mb-4">
            <span v-if="product.stock_quantity > 0" class="inline-block bg-green-100 text-green-700 text-xs font-semibold px-2 py-1 rounded">In Stock</span>
            <span v-else class="inline-block bg-red-100 text-red-700 text-xs font-semibold px-2 py-1 rounded">Out of Stock</span>
          </div>
          <div class="mb-6">
            <p class="text-gray-700 leading-relaxed">{{ product.description }}</p>
          </div>
          <ul v-if="features.length" class="mb-6 space-y-1">
            <li v-for="feature in features" :key="feature" class="text-sm text-gray-600 flex items-center">
              <svg class="h-4 w-4 text-[#ff9900] mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z" clip-rule="evenodd" /></svg>
              {{ feature }}
            </li>
          </ul>
        </div>
        <div class="flex flex-col sm:flex-row items-center gap-4 mt-6">
          <label class="text-sm text-gray-600 mr-2">Quantity:</label>
          <select v-model="quantity" class="border rounded px-2 py-1 w-20 focus:ring-2 focus:ring-[#ff9900]">
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
          <button @click="addToCart" :disabled="product.stock_quantity === 0" class="flex-1 bg-[#ff9900] text-black font-bold py-3 rounded hover:bg-[#e47911] transition text-lg mt-2 sm:mt-0 disabled:opacity-50 disabled:cursor-not-allowed">Add to Cart</button>
        </div>
        <div class="mt-8 text-sm text-gray-500">
          <span>Category: <span class="text-[#232f3e] font-semibold">{{ product.category }}</span></span>
          <span class="ml-4">Manufacturer: <span class="text-[#232f3e] font-semibold">{{ product.manufacturer }}</span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const quantity = ref(1)
const product = ref(null)
const loading = ref(true)
const error = ref('')
const placeholderImg = 'https://via.placeholder.com/320x320?text=No+Image'

const features = computed(() => {
  if (product.value && product.value.metadata && Array.isArray(product.value.metadata.features)) {
    return product.value.metadata.features
  }
  return []
})

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await axios.get(`/api/v1/medicines/${route.params.id}`)
    product.value = data
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Failed to load product.'
  } finally {
    loading.value = false
  }
})

const addToCart = () => {
  // Implement cart functionality
  alert(`Added ${quantity.value} to cart!`)
}
</script> 