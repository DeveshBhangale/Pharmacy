<template>
  <div class="bg-gray-100 min-h-screen">
    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-[#232f3e] to-[#37475a] h-72 flex items-center justify-center mb-12">
      <div class="text-center">
        <h1 class="text-4xl md:text-5xl font-extrabold text-white mb-4 drop-shadow-lg">Welcome to Pharmacy</h1>
        <p class="text-lg md:text-2xl text-[#ff9900] font-semibold mb-6">Your one-stop shop for medicines & health essentials</p>
        <router-link to="/medicines" class="inline-block bg-[#ff9900] text-black font-bold px-8 py-3 rounded hover:bg-[#e47911] transition">Shop Now</router-link>
      </div>
    </div>

    <!-- Category Carousel -->
    <div class="max-w-7xl mx-auto px-4 mb-12">
      <h2 class="text-2xl font-bold mb-4 text-[#232f3e]">Shop by Category</h2>
      <div class="flex space-x-6 overflow-x-auto pb-2 hide-scrollbar">
        <div v-for="category in categories" :key="category.name" class="flex-shrink-0 w-48 bg-white rounded-lg shadow hover:shadow-lg transition p-4 text-center cursor-pointer">
          <img :src="category.image" :alt="category.name" class="h-24 w-24 object-cover mx-auto mb-2 rounded-full border-2 border-[#ff9900]" />
          <div class="font-semibold text-[#232f3e]">{{ category.name }}</div>
        </div>
      </div>
    </div>

    <!-- Featured Products Grid -->
    <div class="max-w-7xl mx-auto px-4 mb-16">
      <h2 class="text-2xl font-bold mb-4 text-[#232f3e]">Featured Products</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        <div v-for="product in featuredProducts" :key="product.id" class="bg-white rounded-lg shadow hover:shadow-xl transition p-4 flex flex-col">
          <img :src="product.image" :alt="product.name" class="h-40 w-full object-contain mb-4 rounded" />
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-[#232f3e] mb-1">{{ product.name }}</h3>
            <p class="text-sm text-gray-500 mb-2">{{ product.category }}</p>
            <div class="flex items-center mb-2">
              <span class="text-[#ff9900] font-bold mr-2">₹{{ product.price }}</span>
              <span class="text-xs text-gray-400">({{ product.rating }}★)</span>
            </div>
          </div>
          <router-link :to="'/medicines/' + product.id" class="mt-2 bg-[#ff9900] text-black font-bold py-2 rounded hover:bg-[#e47911] text-center transition">View Details</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const categories = ref([
  {
    name: 'Medicines',
    image: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    name: 'Supplements',
    image: 'https://images.unsplash.com/photo-1577174881658-0f30ed549adc?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    name: 'Personal Care',
    image: 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    name: 'Medical Devices',
    image: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    name: 'First Aid',
    image: 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
  {
    name: 'Health Food',
    image: 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
  },
])

const featuredProducts = ref([
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
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style> 