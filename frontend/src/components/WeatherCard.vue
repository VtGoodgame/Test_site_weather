<template>
  <div class="bg-lightBlue rounded-xl shadow-lg p-6 w-full max-w-md">
    <!-- Ввод города или координат -->
    <div class="mb-4 flex flex-col gap-2">
      <input v-model="searchQuery" type="text" placeholder="Введите город"
        class="w-full px-4 py-2 rounded-md border border-darkBlue/30 focus:outline-none focus:ring-2 focus:ring-darkBlue" />

      <div class="flex gap-2">
        <input v-model="latitude" type="text" placeholder="Широта (lat)"
          class="w-full px-4 py-2 rounded-md border border-darkBlue/30 focus:outline-none focus:ring-2 focus:ring-darkBlue" />
        <input v-model="longitude" type="text" placeholder="Долгота (lon)"
          class="w-full px-4 py-2 rounded-md border border-darkBlue/30 focus:outline-none focus:ring-2 focus:ring-darkBlue" />
      </div>

      <button @click="onSearch" class="bg-darkBlue text-white px-4 py-2 rounded-md hover:bg-blue-700 transition">
        🔍 Найти
      </button>
    </div>

    <!-- Данные о погоде -->
    <div class="flex items-center justify-between mb-4">
      <img :src="`https://openweathermap.org/img/wn/ ${weather.icon}@2x.png`" alt="weather icon"
        class="w-16 h-16" />
      <div class="text-center">
        <h2 class="text-2xl font-semibold text-darkBlue">{{ weather.city }}</h2>
        <p class="text-darkBlue">Восход: {{ weather.sunrise }} | Закат: {{ weather.sunset }}</p>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 text-darkBlue">
      <div>
        <p class="text-xl">Темп: {{ weather.temperature }}°C</p>
        <p class="text-sm">Мин/Макс: {{ weather.tempMin }}° / {{ weather.tempMax }}°</p>
      </div>
      <div>
        <p>Влажность: {{ weather.humidity }}%</p>
        <p>Ветер: {{ weather.windSpeed }} м/с → {{ weather.windDirection }}</p>
      </div>
    </div>

    <div class="mt-4 text-darkBlue italic text-center">
      <p>{{ weather.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  weather: {
    type: Object,
    required: true
  }
})

// Поля формы
const searchQuery = ref('')
const latitude = ref('')
const longitude = ref('')

// Эмит для родителя
const emit = defineEmits(['search'])

function onSearch() {
  if (latitude.value && longitude.value) {
    // Используем координаты
    emit('search', {
      lat: latitude.value.trim(),
      lon: longitude.value.trim()
    })
  } else if (searchQuery.value.trim()) {
    // Используем название города
    emit('search', { city: searchQuery.value.trim() })
  } else {
    alert('Введите либо город, либо координаты')
  }
}
</script>