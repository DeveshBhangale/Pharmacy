<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <!-- Sticky Amazon-like Header -->
    <header class="sticky top-0 z-50 w-full bg-[#232f3e] text-white shadow">
      <div class="flex items-center px-8 py-2 max-w-7xl mx-auto">
        <!-- Logo -->
        <router-link to="/" class="flex items-center mr-8">
          <img src="@/assets/logo.svg" class="h-10 w-10 mr-2" alt="Pharmacy Logo" />
          <span class="font-bold text-xl tracking-wide">Pharmacy</span>
        </router-link>
        <!-- Category Dropdown -->
        <div
          class="relative mr-6"
          @mouseenter="showCategoryDropdown = true"
          @mouseleave="showCategoryDropdown = false"
        >
          <button :class="['flex items-center px-3 py-2 rounded focus:outline-none transition', showCategoryDropdown ? 'bg-[#232f3e] shadow-lg' : 'bg-[#37475a] hover:bg-[#232f3e]']">
            <svg class="h-5 w-5 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>
            <span class="text-sm">All</span>
            <svg class="h-4 w-4 ml-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd" /></svg>
          </button>
          <transition name="fade-slide">
            <div
              v-if="showCategoryDropdown"
              class="absolute left-0 mt-2 w-48 bg-white text-black rounded shadow-lg z-50 animate-dropdown"
            >
              <router-link to="/medicines" class="block px-4 py-2 hover:bg-gray-100">Medicines</router-link>
              <router-link to="/medicines?category=supplements" class="block px-4 py-2 hover:bg-gray-100">Supplements</router-link>
              <router-link to="/medicines?category=personal-care" class="block px-4 py-2 hover:bg-gray-100">Personal Care</router-link>
              <router-link to="/medicines?category=devices" class="block px-4 py-2 hover:bg-gray-100">Medical Devices</router-link>
            </div>
          </transition>
        </div>
        <!-- Search Bar -->
        <div class="flex-1 flex items-center">
          <input class="w-full px-4 py-2 rounded-l bg-white text-black focus:outline-none" placeholder="Search for medicines, health products..." />
          <button class="bg-[#ff9900] px-6 py-2 rounded-r text-black font-bold hover:bg-[#e47911]">Search</button>
        </div>
        <!-- Account Dropdown -->
        <div
          class="relative ml-8"
          @mouseenter="showAccountDropdown = true"
          @mouseleave="showAccountDropdown = false"
        >
          <button :class="['flex items-center px-3 py-2 rounded focus:outline-none transition', showAccountDropdown ? 'bg-[#232f3e] shadow-lg' : 'bg-[#37475a] hover:bg-[#232f3e]']">
            <svg class="h-5 w-5 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 15c2.485 0 4.797.657 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            <span class="text-sm">Account</span>
            <svg class="h-4 w-4 ml-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd" /></svg>
          </button>
          <transition name="fade-slide">
            <div
              v-if="showAccountDropdown"
              class="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow-lg z-50 animate-dropdown"
            >
              <router-link to="/login" class="block px-4 py-2 hover:bg-gray-100">Sign In</router-link>
              <router-link to="/register" class="block px-4 py-2 hover:bg-gray-100">Register</router-link>
              <router-link to="/orders" class="block px-4 py-2 hover:bg-gray-100">Orders</router-link>
              <router-link to="/profile" class="block px-4 py-2 hover:bg-gray-100">Profile</router-link>
            </div>
          </transition>
        </div>
        <!-- Cart -->
        <router-link to="/cart" class="ml-8 flex items-center hover:text-[#ff9900]">
          <svg class="h-6 w-6 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13l-1.35 2.7A1 1 0 007 17h10a1 1 0 00.95-.68l3.24-7.24A1 1 0 0020 8H6.21" /></svg>
          <span class="font-semibold">Cart</span>
        </router-link>
      </div>
      <!-- Sub-navigation -->
      <nav class="bg-[#37475a] text-white text-sm">
        <div class="max-w-7xl mx-auto px-8 flex space-x-8 h-10 items-center">
          <router-link to="/" class="hover:text-[#ff9900]">Home</router-link>
          <router-link to="/medicines" class="hover:text-[#ff9900]">Medicines</router-link>
          <router-link to="/prescriptions" class="hover:text-[#ff9900]">Prescriptions</router-link>
          <router-link to="/orders" class="hover:text-[#ff9900]">Orders</router-link>
          <router-link to="/profile" class="hover:text-[#ff9900]">Profile</router-link>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-[#232f3e] text-white mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">About Us</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-sm hover:text-[#ff9900]">About Pharmacy</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Careers</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Press Releases</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Customer Service</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Contact Us</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Returns</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Help Center</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Payment Methods</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Credit Cards</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Debit Cards</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Net Banking</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Connect With Us</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Facebook</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Twitter</a></li>
              <li><a href="#" class="text-sm hover:text-[#ff9900]">Instagram</a></li>
            </ul>
          </div>
        </div>
        <div class="mt-8 pt-8 border-t border-gray-700 text-center text-sm">
          <p>&copy; 2024 Pharmacy Management System. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const showCategoryDropdown = ref(false)
const showAccountDropdown = ref(false)
</script>

<style>
@import './assets/tailwind.css';
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.fade-slide-enter-from, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-to, .fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style> 