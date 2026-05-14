import requests
from config import OWM_API_KEY
from .parser import WeatherParser

BASE_URL = "https://api.openweathermap.org/data/2.5"

class WeatherAPI:
    @staticmethod
    def get_current_weather(city_name):
        url = f"{BASE_URL}/weather"
        params = {
            "q": city_name,
            "appid": OWM_API_KEY,
            "units": "metric"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return WeatherParser.parse_current(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current weather: {e}")
            return None

    @staticmethod
    def get_forecast(city_name):
        url = f"{BASE_URL}/forecast"
        params = {
            "q": city_name,
            "appid": OWM_API_KEY,
            "units": "metric"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            weekly = WeatherParser.parse_weekly(data)
            hourly = WeatherParser.parse_hourly(data)
            return weekly, hourly
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return None, None

    @staticmethod
    def get_weather_by_coords(lat, lon):
        url = f"{BASE_URL}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OWM_API_KEY,
            "units": "metric"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            # To match the city flow, we return the parsed name and the weather
            return WeatherParser.parse_current(data), data.get('name')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather by coords: {e}")
            return None, None
