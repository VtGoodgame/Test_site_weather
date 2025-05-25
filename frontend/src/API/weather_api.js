// src/api/weatherApi.js

export async function getWeatherByCity(city) {
  const response = await fetch(`/forecast/${city}`);
  if (!response.ok) throw new Error('Город не найден');
  return await response.json();
}

export async function getWeatherByCoords(lat, lon) {
  const response = await fetch(`/forecast?lat=${lat}&lon=${lon}`);
  if (!response.ok) throw new Error('Координаты не найдены');
  return await response.json();
}