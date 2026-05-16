import sqlite3
import requests
import json
import pandas as pd
from datetime import datetime






class WeatherDataEngine:
    def __init__(self, api_key, db_name="weather_storage.db"):
        self.api_key = api_key
        self.db_name = db_name
        self.__init__db()

    def __init__db(self):
        """Инициализация таблиц в SQLite"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Таблица городов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SavedCities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    lat REAL,
                    lon REAL
                )
            ''')
            # Таблица прогноза
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS WeatherCache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_id INTEGER,
                    date TEXT,
                    day_of_week TEXT,
                    temp REAL,
                    description TEXT,
                    FOREIGN KEY (city_id) REFERENCES SavedCities (id)
                )
            ''')
            conn.commit()

    def get_weather(self, city_name):
        """Основной процесс: получение данных, сохранение в БД и возврат структуры"""
        # 1. Геокодинг (получаем координаты города)
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={self.api_key}"
        geo_res = requests.get(geo_url).json()

        if not geo_res:
            return f"Error: City {city_name} not found."

        city_data = geo_res[0]
        lat, lon = city_data['lat'], city_data['lon']

        # 2. Сохраняем/обновляем город в БД
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO SavedCities (name, lat, lon) VALUES (?, ?, ?)",
                           (city_name, lat, lon))
            cursor.execute("SELECT id FROM SavedCities WHERE name = ?", (city_name,))
            city_id = cursor.fetchone()[0]

            # 3. Получаем прогноз на 5 дней
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={self.api_key}&lang=ru"
            forecast_data = requests.get(forecast_url).json()

            # Очищаем старый кэш для этого города перед обновлением
            cursor.execute("DELETE FROM WeatherCache WHERE city_id = ?", (city_id,))

            processed_forecast = []
            # OpenWeather дает данные каждые 3 часа. Выбираем только прогноз на полдень (12:00)
            for item in forecast_data['list']:
                if "12:00:00" in item['dt_txt']:
                    date_obj = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
                    day_info = {
                        "city_id": city_id,
                        "date": date_obj.strftime('%Y-%m-%d'),
                        "day_of_week": date_obj.strftime('%A'),  # Английское название дня
                        "temp": item['main']['temp'],
                        "description": item['weather'][0]['description']
                    }
                    processed_forecast.append(day_info)

                    # Сохраняем в БД
                    cursor.execute('''
                        INSERT INTO WeatherCache (city_id, date, day_of_week, temp, description)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (day_info['city_id'], day_info['date'], day_info['day_of_week'],
                          day_info['temp'], day_info['description']))

            conn.commit()
            return processed_forecast

    def export_data(self, data, city_name):
        """Экспорт данных в 3 формата"""
        if not data:
            return "No data to export"

        df = pd.DataFrame(data)
        # Убираем city_id из экспорта, пользователю он не нужен
        export_df = df.drop(columns=['city_id'])

        # 1. JSON
        json_file = f"weather_{city_name}.json"
        export_df.to_json(json_file, orient="records", force_ascii=False, indent=4)

        # 2. CSV
        csv_file = f"weather_{city_name}.csv"
        export_df.to_csv(csv_file, index=False, encoding='utf-8-sig')

        # 3. XLSX (Excel)
        xlsx_file = f"weather_{city_name}.xlsx"
        export_df.to_excel(xlsx_file, index=False)

        print(f"Экспорт завершен: {json_file}, {csv_file}, {xlsx_file}")


# --- ПРИМЕР РАБОТЫ ---
if __name__ == "__main__":
    API_KEY = "5b70fa7ad437c5f31b33c2ea56b8b5ac"
    engine = WeatherDataEngine(API_KEY)

    city = "Moscow"  # Можно подставить любой город
    print(f"Запрос данных для города: {city}...")

    weather_data = engine.get_weather(city)

    if isinstance(weather_data, list):
        engine.export_data(weather_data, city)
        print("Данные успешно сохранены в БД и файлы.")
    else:
        print(weather_data)
