<template>
  <div class="min-h-screen bg-pastelBlue flex items-center justify-center p-4">
    <WeatherCard />
    <!-- <forecast /> -->
  </div>
</template>

<script setup>
import WeatherCard from './components/WeatherCard.vue'
import forecast from './components/Weather_forecast.vue'
import { ref } from 'vue'

const weatherData = ref({})

</script>