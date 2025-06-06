<template>
  <div class="bg-white">
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
          <h1 class="text-2xl font-semibold leading-6 text-gray-900">Prescriptions</h1>
          <p class="mt-2 text-sm text-gray-700">
            A list of all your uploaded prescriptions and their status.
          </p>
        </div>
        <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <router-link
            to="/prescriptions/upload"
            class="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Upload Prescription
          </router-link>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="mt-8 text-center">
        <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-indigo-600 border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
          <span class="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">Loading...</span>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="mt-8 text-center text-red-600">
        {{ error }}
      </div>

      <!-- Empty state -->
      <div v-else-if="prescriptions.length === 0" class="mt-8 text-center text-gray-500">
        <p>You haven't uploaded any prescriptions yet.</p>
        <router-link
          to="/prescriptions/upload"
          class="mt-4 inline-block text-indigo-600 hover:text-indigo-500"
        >
          Upload your first prescription
        </router-link>
      </div>

      <!-- Prescriptions list -->
      <div v-else class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                      Date
                    </th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Doctor
                    </th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Status
                    </th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Items
                    </th>
                    <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span class="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                  <tr v-for="prescription in prescriptions" :key="prescription.id">
                    <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                      {{ new Date(prescription.created_at).toLocaleDateString() }}
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      {{ prescription.doctor_name }}
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm">
                      <span
                        :class="[
                          prescription.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                          prescription.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                          prescription.status === 'completed' ? 'bg-green-100 text-green-800' :
                          'bg-red-100 text-red-800',
                          'inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset'
                        ]"
                      >
                        {{ prescription.status.charAt(0).toUpperCase() + prescription.status.slice(1) }}
                      </span>
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      {{ prescription.items_count }} items
                    </td>
                    <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                      <button
                        @click="viewPrescription(prescription)"
                        class="text-indigo-600 hover:text-indigo-900"
                      >
                        View<span class="sr-only">, {{ prescription.id }}</span>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Prescription details modal -->
    <div v-if="selectedPrescription" class="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
            <div>
              <div class="mt-3 text-center sm:mt-5">
                <h3 class="text-base font-semibold leading-6 text-gray-900" id="modal-title">
                  Prescription Details
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    Doctor: {{ selectedPrescription.doctor_name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    Date: {{ new Date(selectedPrescription.created_at).toLocaleDateString() }}
                  </p>
                  <p class="text-sm text-gray-500">
                    Status: {{ selectedPrescription.status }}
                  </p>
                </div>
              </div>
            </div>
            <div class="mt-5 sm:mt-6">
              <button
                type="button"
                class="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                @click="selectedPrescription = null"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Prescription {
  id: number
  doctor_name: string
  status: 'pending' | 'processing' | 'completed' | 'rejected'
  created_at: string
  items_count: number
}

const prescriptions = ref<Prescription[]>([])
const selectedPrescription = ref<Prescription | null>(null)
const loading = ref(true)
const error = ref('')

const fetchPrescriptions = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await axios.get('/api/v1/prescriptions')
    prescriptions.value = response.data
  } catch (err) {
    error.value = 'Failed to load prescriptions. Please try again later.'
    console.error('Error fetching prescriptions:', err)
  } finally {
    loading.value = false
  }
}

const viewPrescription = (prescription: Prescription) => {
  selectedPrescription.value = prescription
}

onMounted(() => {
  fetchPrescriptions()
})
</script> 