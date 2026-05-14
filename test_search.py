import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'weather_app'))
from api.weather_api import WeatherAPI
import config

config.OWM_API_KEY = "f0070f4e338513f27ceb7f7f67f1bb47"

try:
    current = WeatherAPI.get_current_weather("London")
    print("Current:", current)
except Exception as e:
    print("Error:", e)
