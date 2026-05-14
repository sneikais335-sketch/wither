from .db_manager import DBManager
import datetime
import sqlite3

class CalendarDB:
    @staticmethod
    def add_event(date, title, note=""):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO calendar_events (date, title, note, created_at)
                VALUES (?, ?, ?, ?)
            ''', (date, title, note, now))
            conn.commit()

    @staticmethod
    def get_events(date=None):
        with DBManager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if date:
                cursor.execute("SELECT * FROM calendar_events WHERE date = ? ORDER BY created_at ASC", (date,))
            else:
                cursor.execute("SELECT * FROM calendar_events ORDER BY date ASC, created_at ASC")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def delete_event(event_id):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM calendar_events WHERE id = ?", (event_id,))
            conn.commit()
