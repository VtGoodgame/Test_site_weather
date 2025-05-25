from dotenv import load_dotenv
import os

load_dotenv()

Api_key = os.getenv('API_key')
COOKIE_NAME = "access_token"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
Five_day_forecast_URL = "https://api.openweathermap.org/data/2.5/forecast"