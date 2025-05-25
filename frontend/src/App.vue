<template>
  <div class="min-h-screen bg-pastelBlue flex items-center justify-center p-4">
    <WeatherCard :weather="weatherData" @search="handleCitySearch" />
  </div>
</template>

<script setup>
import WeatherCard from './components/WeatherCard.vue'
import { ref } from 'vue'

const weatherData = ref({
  city: 'Введите город',
  temperature: 22,
  tempMin: 18,
  tempMax: 25,
  humidity: 65,
  windSpeed: 5,
  windDirection: 'СВ',
  sunrise: '06:15',
  sunset: '20:45',
  description: 'Облачно с прояснениями',
  icon: '01d'
})

// TODO: под подключение к API
async function handleCitySearch(params) {
  try {
    let url;

    if (params.city) {
      url = `http://localhost:8000/${encodeURIComponent(params.city)}`;
      console.log(url);
    } else if (params.lat && params.lon) {
      url = `http://localhost:8000/?lat=${params.lat}&lon=${params.lon}`;
      console.log(url);
    } else {
      alert('Введите город или координаты');
      return;
    }

    const response = await fetch(url);
    console.log(response);  

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Ошибка загрузки погоды');
    }

    const data = await response.json();
    console.log(data);
    const today = data.forecast;

    // ✅ Обновляем состояние
    weatherData.value = {
      city: data.city,
      temperature: Math.round(today.temperature),
      tempMin: Math.round(today.temperature - 2),
      tempMax: Math.round(today.temperature + 2),
      humidity: today.humidity,
      windSpeed: today.wind_speed,
      windDirection: 'СВ',
      sunrise: '06:00',
      sunset: '18:00',
      description: today.description,
      icon: today.icon
    };

  } catch (error) {
    alert(error.message);
  }
}

/**
 * Получает прогноз погоды для города через FastAPI
 * @param {Object} params - Параметры запроса
 * @param {string} [params.city] - Название города
 * @returns {Promise<Object>} - Данные о погоде
 */
async function get_weather_fetch(params) {
  // Проверяем, передан ли город
  if (!params.city) {
    throw new Error('Для получения прогноза необходимо указать город');
  }

  // Формируем URL
  const url = `http://localhost:8000/forecast/${encodeURIComponent(params.city)}`;

  // Делаем запрос
  const response = await fetch(url);

  // Обрабатываем ошибки
  if (!response.ok) {
    let errorMessage = 'Ошибка загрузки погоды';

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (e) {
      console.error(e);
    }

    throw new Error(errorMessage);
  }

  // Возвращаем данные
  return await response.json();
}
</script>
