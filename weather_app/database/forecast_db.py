from .db_manager import DBManager
import datetime
import sqlite3

class ForecastDB:
    @staticmethod
    def save_weekly_forecast(city_name, forecast_list):
        """
        Save weekly forecast. Replaces existing forecast for the city.
        forecast_list: list of dicts matching columns
        """
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM weekly_forecast WHERE city_name = ?", (city_name,))
            
            now = datetime.datetime.now().isoformat()
            for day in forecast_list:
                cursor.execute('''
                    INSERT INTO weekly_forecast (
                        city_name, date, day_name, condition, icon_code,
                        temp_min, temp_max, humidity, wind_speed, pressure,
                        visibility, dew_point, uv_index, cached_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    city_name, day.get('date'), day.get('day_name'), day.get('condition'),
                    day.get('icon_code'), day.get('temp_min'), day.get('temp_max'),
                    day.get('humidity'), day.get('wind_speed'), day.get('pressure'),
                    day.get('visibility'), day.get('dew_point'), day.get('uv_index'), now
                ))
            conn.commit()

    @staticmethod
    def get_weekly_forecast(city_name):
        with DBManager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM weekly_forecast WHERE city_name = ? ORDER BY date ASC", (city_name,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def save_hourly_forecast(city_name, hourly_list):
        """
        Save hourly forecast. Replaces existing forecast for the city.
        hourly_list: list of dicts matching columns
        """
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hourly_forecast WHERE city_name = ?", (city_name,))
            
            now = datetime.datetime.now().isoformat()
            for hour in hourly_list:
                cursor.execute('''
                    INSERT INTO hourly_forecast (
                        city_name, datetime, temp, condition, icon_code, cached_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    city_name, hour.get('datetime'), hour.get('temp'),
                    hour.get('condition'), hour.get('icon_code'), now
                ))
            conn.commit()

    @staticmethod
    def get_hourly_forecast(city_name):
        with DBManager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hourly_forecast WHERE city_name = ? ORDER BY datetime ASC", (city_name,))
            return [dict(row) for row in cursor.fetchall()]
