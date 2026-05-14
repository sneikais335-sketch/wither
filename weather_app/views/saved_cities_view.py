import customtkinter as ctk
from config import COLORS, FONTS
from components.city_card import CityCard
from database.cities_db import CitiesDB

class SavedCitiesView(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_page"], **kwargs)
        self.app = app_controller

        self.container = ctk.CTkFrame(self, width=900, fg_color="transparent")
        self.container.place(relx=0.5, rely=0, anchor="n", relheight=1)
        self.container.pack_propagate(False)

        self._build_header()
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, pady=20)
        
        # Will be populated on load
        self.empty_label = None

    def _build_header(self):
        header = ctk.CTkFrame(self.container, height=80, fg_color="transparent")
        header.pack(fill="x", pady=(20, 0))
        header.pack_propagate(False)

        btn_back = ctk.CTkButton(
            header, text="← Back", width=60, fg_color="transparent", 
            text_color=COLORS["text_primary"], font=FONTS["btn_text"],
            hover_color=COLORS["menu_item_hover"], command=lambda: self.app.show_view("main")
        )
        btn_back.pack(side="left", padx=(0, 20))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")

        self.lbl_title = ctk.CTkLabel(title_frame, text=self.app.lang.t("saved_cities"), text_color=COLORS["accent_blue"], font=FONTS["title_large"])
        self.lbl_title.pack(anchor="w")

    def load_cities(self):
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cities = CitiesDB.get_all_cities()
        if not cities:
            self._show_empty()
            return

        row = 0
        col = 0
        for city in cities:
            # We need to fetch recent forecast for these cities. 
            # In a real app we might fetch from DB or API asynchronously.
            # Here we just use the name and wait for a click, or use placeholder data if we don't have current weather.
            # We'll use get_weather_sync from API for demonstration if not cached, 
            # but to avoid blocking UI, we'll try to get from forecast_db or just show the name.
            # For simplicity, we just show the name and placeholders until clicked.
            # In production, we'd fetch current weather for all saved cities on background thread.
            
            card = CityCard(
                self.scrollable_frame, 
                on_click_callback=self._on_city_click,
                on_delete_callback=self._on_city_delete
            )
            card.grid(row=row, column=col, padx=15, pady=15)
            
            # Placeholder data update
            card.update_data(
                city['id'], city['name'], 0, "Loading...", 0, 0, 0
            )
            
            # Fetch actual data (simplified sync fetch, ideally async)
            current_data = self.app.fetch_current_weather_sync(city['name'])
            if current_data:
                card.update_data(
                    city['id'], city['name'], current_data['temp'], 
                    self.app.lang.t(f"conditions.{current_data['condition']}"), 
                    current_data['feels_like'], current_data['humidity'], current_data['wind_speed']
                )

            col += 1
            if col > 2: # 3 cards per row
                col = 0
                row += 1

    def _show_empty(self):
        self.empty_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text=self.app.lang.t("no_cities") + "\n\n" + self.app.lang.t("no_cities_sub"),
            text_color=COLORS["text_secondary"], font=FONTS["subtitle"],
            justify="center"
        )
        self.empty_label.pack(pady=100)

    def _on_city_click(self, city_name):
        self.app.load_weather(city_name)
        self.app.show_view("main")

    def _on_city_delete(self, city_id):
        CitiesDB.delete_city(city_id)
        self.load_cities() # Reload the view

    def refresh_texts(self):
        self.lbl_title.configure(text=self.app.lang.t("saved_cities"))
        self.load_cities()
