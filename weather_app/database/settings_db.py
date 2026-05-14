from .db_manager import DBManager
import sqlite3

class SettingsDB:
    @staticmethod
    def get_settings():
        with DBManager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM app_settings WHERE id = 1")
            row = cursor.fetchone()
            return dict(row) if row else {}

    @staticmethod
    def update_setting(key, value):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            # Basic validation
            allowed_keys = ['language', 'temp_unit', 'default_city', 'notifications_enabled', 'auto_location']
            if key in allowed_keys:
                cursor.execute(f"UPDATE app_settings SET {key} = ? WHERE id = 1", (value,))
                conn.commit()
