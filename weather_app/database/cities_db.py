from .db_manager import DBManager
import datetime

class CitiesDB:
    @staticmethod
    def add_city(name, country="", lat=None, lon=None):
        """Add a new city if it doesn't already exist."""
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if exists
            cursor.execute("SELECT id FROM saved_cities WHERE name = ? COLLATE NOCASE", (name,))
            if cursor.fetchone():
                return False # Already exists
                
            now = datetime.datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO saved_cities (name, country, lat, lon, saved_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, country, lat, lon, now))
            conn.commit()
            return True

    @staticmethod
    def get_all_cities():
        """Get all saved cities."""
        with DBManager.get_connection() as conn:
            conn.row_factory = sqlite3.Row if 'sqlite3' in globals() else None
            # Need to import sqlite3 if using row_factory, let's just return dicts manually
            import sqlite3
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM saved_cities ORDER BY saved_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def delete_city(city_id):
        """Delete a saved city by ID."""
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM saved_cities WHERE id = ?", (city_id,))
            conn.commit()
