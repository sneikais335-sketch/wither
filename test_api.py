import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'weather_app'))
from api.weather_api import WeatherAPI
from api.parser import WeatherParser
import requests

API_KEY = "f0070f4e338513f27ceb7f7f67f1bb47"

try:
    url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}&units=metric"
    res = requests.get(url)
    res.raise_for_status()
    raw = res.json()
    print("CURRENT PARSED:", WeatherParser.parse_current(raw))

    url2 = f"https://api.openweathermap.org/data/2.5/forecast?q=London&appid={API_KEY}&units=metric"
    res2 = requests.get(url2)
    res2.raise_for_status()
    raw2 = res2.json()
    print("HOURLY PARSED:", len(WeatherParser.parse_hourly(raw2)))
    print("WEEKLY PARSED:", len(WeatherParser.parse_weekly(raw2)))

except Exception as e:
    print("TEST ERROR:", e)
