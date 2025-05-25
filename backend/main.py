import os
import requests
from datetime import datetime
from urllib.parse import quote, unquote, parse_qs
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query, Response, Request
import consts as c

WEATHER_URL = c.WEATHER_URL
API_KEY = c.Api_key
app = FastAPI(
    title="Прогноз погоды API",
    description="Получение прогноза погоды на 5 дней через OpenWeatherMap (бесплатный тариф)",
    version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # порт твоего Vue-приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def  add_cookies(response: Response,city: str = None, lat: str = None, lon: str = None):
    encoded_city =quote(city) if city else ""
    encoded_lat = quote(lat) if lat else ""
    encoded_lon = quote(lon) if lon else "" 
    cookie_value = f"city={encoded_city}&lat={encoded_lat}&lon={encoded_lon}"
    response.set_cookie(
        key=c.COOKIE_NAME,
        value=cookie_value,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )
    return response

def get_weather_forecast(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",   # Градусы Цельсия
        "lang": "ru",        # Ответ на русском
        "cnt": 40            # Максимум записей (прогноз каждые 3 часа)
    }

    response = requests.get(c.Five_day_forecast_URL, params=params)

    if response.status_code != 200:
        return None, response.json().get("message", "Неизвестная ошибка")

    data = response.json()
    # Группируем по дням (берём первую запись каждого дня)
    forecast_by_day = {}

    for entry in data["list"]: #data["list"] — это массив из ~40 элементов. Каждый элемент — прогноз на определённое время (например, "2025-04-06 12:00")
        dt = datetime.fromtimestamp(entry["dt"]) #entry["dt"] — временная метка в секундах (Unix timestamp), которую мы переводим в читаемую дату с помощью datetime.fromtimestamp.
        date_str = dt.strftime("%Y-%m-%d")#date_str — строка вида '2025-04-06', т.е. только дата без времени

        if date_str not in forecast_by_day:
            forecast_by_day[date_str] = {
                "date": date_str,
                "temperature": entry["main"]["temp"],
                "feels_like": entry["main"]["feels_like"],
                "description": entry["weather"][0]["description"].capitalize(),
                "wind_speed": entry["wind"]["speed"],
                "humidity": entry["main"]["humidity"],
                "pressure": entry["main"]["pressure"]
            }

    # Сортируем и берем первые 5 дней
    sorted_forecast = sorted(forecast_by_day.values(), key=lambda x: x["date"])[:5]

    return sorted_forecast, None


@app.get("/", summary="Получить прогноз погоды на сегодняшний день")
async def root(
    request: Request,
    city: str = Query(None),
    lat: str = Query(None),
    lon: str = Query(None),
    api_key: str = Query(default=c.Api_key)
):
    """
    Получает прогноз погоды на сегодняшний день для указанного города.
    
    - **city**: Название города 
    - **lat**: Широта  (необязательные параметры для поиска погоды по конкретному месту на карте)
    - **lon**: Долгота (необязательные параметры для поиска погоды по конкретному месту на карте)
    - Возвращает температуру, описание погоды, ветер и др.
    """
    try:
        # Получаем куки
        cookie_data = request.cookies.get(c.COOKIE_NAME)
        cookie_city = cookie_lat = cookie_lon = ""

        if cookie_data:
            decoded_cookie = unquote(cookie_data)
            parsed = parse_qs(decoded_cookie)
            cookie_city = parsed.get("city", [""])[0]
            cookie_lat = parsed.get("lat", [""])[0]
            cookie_lon = parsed.get("lon", [""])[0]

        # Приоритет: параметры запроса > куки
        if not (city or lat or lon):
            city = cookie_city
            lat = cookie_lat
            lon = cookie_lon

        # Проверяем, получили ли мы нужные данные
        if not (city or (lat and lon)):
            raise HTTPException(status_code=400, detail="Не указаны ни город, ни координаты")

        # Формируем параметры запроса
        params = {"appid": api_key, "units": "metric", "lang": "ru"}
        if lat and lon:
            params.update({"lat": lat, "lon": lon})
        else:
            params["q"] = city

        # Запрос к API погоды
        response = requests.get(WEATHER_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Город или координаты не найдены")

        weather_data = response.json()

        # Создаем JSON-ответ и обновляем куки с новыми данными
        json_response = JSONResponse(content=weather_data)
        await add_cookies(json_response, city=city, lat=lat, lon=lon)
        return json_response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ошибка при обращении к сервису погоды: {e}")
    

@app.get("/forecast/{city}", summary="Получить прогноз погоды на 5 дней")
async def forecast(request: Request, city: str = None):
    """
    Получает прогноз погоды на 5 дней для указанного города.
    
    - **city**: Название города (например, Москва)
    - Возвращает температуру, описание погоды, ветер и др.
    """
    try:
        # Получаем куки
        cookie_data = request.cookies.get(c.COOKIE_NAME)
        cookie_city = cookie_lat = cookie_lon = ""

        if cookie_data:
            decoded_cookie = unquote(cookie_data)
            parsed = parse_qs(decoded_cookie)
            cookie_city = parsed.get("city", [""])[0]
            cookie_lat = parsed.get("lat", [""])[0]
            cookie_lon = parsed.get("lon", [""])[0]

        # Приоритет: параметры запроса > куки
        if not city:
            city = cookie_city

        forecast_data, error = get_weather_forecast(city)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "city": city.capitalize(),
            "forecast": forecast_data
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ошибка при обращении к сервису погоды: {e}")
    
    