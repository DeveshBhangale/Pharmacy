<template>
  <div class="bg-white">
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div class="mx-auto max-w-2xl">
        <h1 class="text-2xl font-semibold leading-6 text-gray-900">Upload Prescription</h1>
        <p class="mt-2 text-sm text-gray-700">
          Upload your prescription and we'll process it for you.
        </p>

        <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
          <div>
            <label for="doctor_name" class="block text-sm font-medium leading-6 text-gray-900">
              Doctor's Name
            </label>
            <div class="mt-2">
              <input
                id="doctor_name"
                v-model="doctorName"
                name="doctor_name"
                type="text"
                required
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label for="prescription_file" class="block text-sm font-medium leading-6 text-gray-900">
              Prescription File
            </label>
            <div class="mt-2">
              <div
                class="flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10"
                :class="{ 'border-indigo-600': isDragging }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleFileDrop"
              >
                <div class="text-center">
                  <svg
                    class="mx-auto h-12 w-12 text-gray-300"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <div class="mt-4 flex text-sm leading-6 text-gray-600">
                    <label
                      for="file-upload"
                      class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        type="file"
                        accept=".pdf,.jpg,.jpeg,.png"
                        class="sr-only"
                        @change="handleFileSelect"
                      />
                    </label>
                    <p class="pl-1">or drag and drop</p>
                  </div>
                  <p class="text-xs leading-5 text-gray-600">PDF, JPG, PNG up to 10MB</p>
                </div>
              </div>
            </div>
            <p v-if="selectedFile" class="mt-2 text-sm text-gray-500">
              Selected file: {{ selectedFile.name }}
            </p>
          </div>

          <div>
            <label for="notes" class="block text-sm font-medium leading-6 text-gray-900">
              Additional Notes
            </label>
            <div class="mt-2">
              <textarea
                id="notes"
                v-model="notes"
                name="notes"
                rows="3"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              ></textarea>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading || !isFormValid"
              class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Uploading...</span>
              <span v-else>Upload Prescription</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const doctorName = ref('')
const selectedFile = ref<File | null>(null)
const notes = ref('')
const loading = ref(false)
const isDragging = ref(false)

const isFormValid = computed(() => {
  return doctorName.value.length > 0 && selectedFile.value !== null
})

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    selectedFile.value = input.files[0]
  }
}

const handleFileDrop = (event: DragEvent) => {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value || !selectedFile.value) return

  try {
    loading.value = true

    // Create form data
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('doctor_name', doctorName.value)
    if (notes.value) {
      formData.append('notes', notes.value)
    }

    // Upload prescription
    await axios.post('/api/v1/prescriptions/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Redirect to prescriptions list
    router.push('/prescriptions')
  } catch (error) {
    console.error('Error uploading prescription:', error)
    // TODO: Show error message to user
  } finally {
    loading.value = false
  }
}
</script> 