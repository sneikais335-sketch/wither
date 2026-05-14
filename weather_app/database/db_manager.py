import sqlite3
import os

DB_NAME = "weather_app.db"

class DBManager:
    """Manages SQLite connection and table creation."""
    
    @staticmethod
    def get_connection():
        # Ensure database is created in the app root, not current working directory if run from elsewhere
        # However, relying on DB_NAME in CWD for simplicity as per standard desktop app setup.
        return sqlite3.connect(DB_NAME)

    @staticmethod
    def initialize():
        """Create all tables if they do not exist."""
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. saved_cities
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    country TEXT,
                    lat REAL,
                    lon REAL,
                    saved_at TEXT
                )
            ''')
            
            # 2. weekly_forecast
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_forecast (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    day_name TEXT,
                    condition TEXT,
                    icon_code TEXT,
                    temp_min REAL,
                    temp_max REAL,
                    humidity INTEGER,
                    wind_speed REAL,
                    pressure INTEGER,
                    visibility REAL,
                    dew_point REAL,
                    uv_index REAL,
                    cached_at TEXT
                )
            ''')
            
            # 3. hourly_forecast
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hourly_forecast (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_name TEXT NOT NULL,
                    datetime TEXT NOT NULL,
                    temp REAL,
                    condition TEXT,
                    icon_code TEXT,
                    cached_at TEXT
                )
            ''')
            
            # 4. calendar_events
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calendar_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    title TEXT NOT NULL,
                    note TEXT,
                    created_at TEXT
                )
            ''')
            
            # 5. app_settings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_settings (
                    id INTEGER PRIMARY KEY,
                    language TEXT,
                    temp_unit TEXT,
                    default_city TEXT,
                    notifications_enabled INTEGER,
                    auto_location INTEGER
                )
            ''')
            
            # Insert default settings if table is empty
            cursor.execute("SELECT COUNT(*) FROM app_settings")
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO app_settings (id, language, temp_unit, default_city, notifications_enabled, auto_location)
                    VALUES (1, 'en', 'C', 'London', 1, 0)
                ''')
            
            conn.commit()

# Run initialization when module is imported
DBManager.initialize()
