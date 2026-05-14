import customtkinter as ctk
import datetime
from config import SIZES, COLORS
from utils.language import LanguageManager
from database.settings_db import SettingsDB
from database.cities_db import CitiesDB
from database.forecast_db import ForecastDB
from api.weather_api import WeatherAPI
from views.main_view import MainView
from views.menu_panel import MenuPanel
from views.saved_cities_view import SavedCitiesView
from views.settings_view import SettingsView
from views.calendar_view import CalendarView
from components.export_dialog import ExportDialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Load Settings
        self.settings = SettingsDB.get_settings()
        
        # Load Language
        self.lang = LanguageManager()
        self.lang.load(self.settings.get('language', 'en'))
        
        self.title(self.lang.t("app_title"))
        self.geometry(f"{SIZES['window_default'][0]}x{SIZES['window_default'][1]}")
        self.minsize(SIZES['window_min'][0], SIZES['window_min'][1])
        self.configure(fg_color=COLORS["bg_page"])

        self.current_city = self.settings.get('default_city', 'London')
        
        self._build_views()
        self.show_view("main")
        
        # Initial data load
        if self.settings.get('auto_location'):
            self.detect_location()
        else:
            self.load_weather(self.current_city)

    def _build_views(self):
        self.views = {}
        
        # Main View
        self.views["main"] = MainView(self, self)
        
        # Saved Cities View
        self.views["saved"] = SavedCitiesView(self, self)
        
        # Settings View
        self.views["settings"] = SettingsView(self, self)
        
        # Menu Panel (Overlay)
        self.menu = MenuPanel(self, self)
        self.menu_visible = False

    def show_view(self, view_name):
        for v in self.views.values():
            v.place_forget()
            
        self.views[view_name].place(x=0, y=0, relwidth=1, relheight=1)
        if view_name == "saved":
            self.views["saved"].load_cities()
            
    def toggle_menu(self):
        if self.menu_visible:
            self.menu.place_forget()
            self.menu_visible = False
        else:
            # Place floating below the header/hamburger icon
            # Approximation based on standard window sizes and header padding
            # We also give it a high z-index (lift)
            self.menu.place(x=60, y=80)
            self.menu.lift()
            self.menu_visible = True

    def show_calendar(self):
        CalendarView(self, self)

    def show_export_dialog(self):
        ExportDialog(self, self)

    def fetch_current_weather_sync(self, city_name):
        """Helper to get current weather synchronously for other views."""
        return WeatherAPI.get_current_weather(city_name)

    def load_weather(self, city_name):
        self.current_city = city_name
        
        # Simple caching logic check:
        # Check if we have recent data in DB (within 30 mins)
        weekly = ForecastDB.get_weekly_forecast(city_name)
        hourly = ForecastDB.get_hourly_forecast(city_name)
        
        use_cache = False
        if weekly and hourly:
            cached_time_str = weekly[0].get('cached_at')
            if cached_time_str:
                cached_time = datetime.datetime.fromisoformat(cached_time_str)
                if (datetime.datetime.now() - cached_time).total_seconds() < 1800:
                    use_cache = True

        if use_cache:
            current = self.fetch_current_weather_sync(city_name) # Always fetch current, or mock from first hourly
            self.views["main"].update_view(current, weekly, hourly)
        else:
            # Fetch from API
            current = WeatherAPI.get_current_weather(city_name)
            weekly, hourly = WeatherAPI.get_forecast(city_name)
            
            if weekly:
                ForecastDB.save_weekly_forecast(city_name, weekly)
            if hourly:
                ForecastDB.save_hourly_forecast(city_name, hourly)
                
            self.views["main"].update_view(current, weekly, hourly)
            
        # Update default city if needed
        SettingsDB.update_setting('default_city', city_name)

    def save_city(self, city_name):
        # We need coords, we'll try to get them from current weather or ignore for now
        CitiesDB.add_city(city_name)

    def detect_location(self):
        # Mocking location detection to London for now
        # Ideally use an IP-based location service
        self.load_weather("London")

    def switch_language(self, code):
        self.lang.switch(code, self)
        SettingsDB.update_setting('language', code)
        self.title(self.lang.t("app_title"))

    def refresh_all_texts(self):
        self.views["main"].refresh_texts()
        self.views["saved"].refresh_texts()
        self.views["settings"].refresh_texts()
        self.menu.refresh_texts()
        self.title(self.lang.t("app_title"))
