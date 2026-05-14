import customtkinter as ctk
import datetime
from config import COLORS, FONTS, SIZES
from components.weather_card import WeatherCard
from components.stat_tile import StatTile
from components.hourly_chart import HourlyChart
from components.weekly_row import WeeklyRow

class MainView(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_page"], **kwargs)
        self.app = app_controller
        
        # Use a scrollable frame for the whole view
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        # Inner container for fixed width (900px)
        self.container = ctk.CTkFrame(self.scroll_frame, width=900, fg_color="transparent")
        self.container.pack(pady=20, anchor="center")
        
        # CTkFrame with fixed width needs pack_propagate(False) if we want to enforce it, 
        # but if we let children dictate height, we don't need height.
        # However, to enforce width=900, we might need a trick if pack ignores width.
        # Actually, CTkFrame width works if we don't pack(fill="x").
        
        self._build_header()
        self._build_search()
        self._build_content()

    def _build_header(self):
        header = ctk.CTkFrame(self.container, width=900, height=80, fg_color="transparent")
        header.pack(pady=(0, 20))
        header.pack_propagate(False)

        # Menu button (left)
        self.btn_menu = ctk.CTkButton(
            header, text="☰", width=50, height=50, font=("Segoe UI", 24),
            fg_color=COLORS["bg_card"], text_color=COLORS["text_primary"],
            corner_radius=15, command=self.app.toggle_menu
        )
        self.btn_menu.place(x=0, rely=0.5, anchor="w")

        # Titles (centered)
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        self.lbl_title_w = ctk.CTkLabel(title_frame, text="Weather", text_color=COLORS["accent_blue"], font=FONTS["title_large"])
        self.lbl_title_w.pack(side="left")
        
        self.lbl_title_f = ctk.CTkLabel(title_frame, text=" Forecast", text_color=COLORS["accent_purple"], font=FONTS["title_large"])
        self.lbl_title_f.pack(side="left")

        self.lbl_subtitle = ctk.CTkLabel(
            header, text=self.app.lang.t("app_subtitle"), 
            text_color=COLORS["text_secondary"], font=FONTS["subtitle"]
        )
        self.lbl_subtitle.place(relx=0.5, rely=0.8, anchor="center")

        # Calendar trigger (right)
        self.btn_calendar = ctk.CTkButton(
            header, text="📅 " + datetime.datetime.now().strftime("%d.%m.%Y"),
            width=120, height=40,
            fg_color=COLORS["bg_card"], text_color=COLORS["text_primary"],
            font=FONTS["btn_text"], hover_color=COLORS["menu_item_hover"],
            corner_radius=10, command=self.app.show_calendar
        )
        self.btn_calendar.place(relx=1.0, rely=0.5, anchor="e")

    def _build_search(self):
        search_frame = ctk.CTkFrame(self.container, width=900, height=50, fg_color="transparent")
        search_frame.pack(pady=(0, 30))
        search_frame.pack_propagate(False)
        
        inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        # Pill shape container
        pill = ctk.CTkFrame(inner, height=50, fg_color=COLORS["bg_card"], corner_radius=25)
        pill.pack(side="left")

        # Search icon
        lbl_icon = ctk.CTkLabel(pill, text="🔍", text_color=COLORS["text_secondary"])
        lbl_icon.pack(side="left", padx=(20, 5))

        self.search_entry = ctk.CTkEntry(
            pill, width=300, height=50, placeholder_text=self.app.lang.t("search_placeholder"),
            font=FONTS["search_input"], fg_color=COLORS["bg_card"], text_color=COLORS["text_primary"],
            border_width=0
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self._on_search())

        self.btn_search = ctk.CTkButton(
            pill, text=self.app.lang.t("search_btn"), width=100, height=40,
            font=FONTS["btn_text"], fg_color=COLORS["btn_search_bg"], text_color=COLORS["text_white"],
            corner_radius=20, command=self._on_search
        )
        self.btn_search.pack(side="left", padx=(0, 5), pady=5)

    def _build_content(self):
        # Main Card
        self.main_card = WeatherCard(self.container)
        self.main_card.pack(pady=(0, 20))

        # Stat Tiles row
        self.tiles_frame = ctk.CTkFrame(self.container, width=900, height=SIZES["stat_tile_h"], fg_color="transparent")
        self.tiles_frame.pack(pady=(0, 20))
        self.tiles_frame.pack_propagate(False)
        
        # We need to distribute 6 tiles evenly
        # 6 * 130 = 780. 900 - 780 = 120 / 5 = 24px gap
        
        self.t_hum = StatTile(self.tiles_frame, COLORS["icon_humidity"], "💧", self.app.lang.t("humidity"), "--%")
        self.t_hum.pack(side="left")
        
        self.t_wind = StatTile(self.tiles_frame, COLORS["icon_wind"], "💨", self.app.lang.t("wind_speed"), "--")
        self.t_wind.pack(side="left", padx=(24, 0))
        
        self.t_vis = StatTile(self.tiles_frame, COLORS["icon_visibility"], "👁", self.app.lang.t("visibility"), "--")
        self.t_vis.pack(side="left", padx=(24, 0))
        
        self.t_pres = StatTile(self.tiles_frame, COLORS["icon_pressure"], "⏱", self.app.lang.t("pressure"), "--")
        self.t_pres.pack(side="left", padx=(24, 0))
        
        self.t_dew = StatTile(self.tiles_frame, COLORS["icon_dew"], "🌡", self.app.lang.t("dew_point"), "--")
        self.t_dew.pack(side="left", padx=(24, 0))
        
        self.t_uv = StatTile(self.tiles_frame, COLORS["icon_uv"], "☀", self.app.lang.t("uv_index"), "--")
        self.t_uv.pack(side="left", padx=(24, 0))

        # Today's Temperature Card
        today_card = ctk.CTkFrame(self.container, width=900, fg_color=COLORS["bg_card"], corner_radius=20)
        today_card.pack(pady=(0, 20), fill="x")
        
        lbl_today = ctk.CTkLabel(
            today_card, text=self.app.lang.t("today_temp"), 
            font=FONTS["section_head"], text_color=COLORS["text_primary"]
        )
        lbl_today.pack(anchor="w", padx=20, pady=(20, 10))

        self.hourly_chart = HourlyChart(today_card)
        self.hourly_chart.pack(fill="x", padx=20, pady=(0, 20))

        # 7-Day Forecast Card
        week_card = ctk.CTkFrame(self.container, width=900, fg_color=COLORS["bg_card"], corner_radius=20)
        week_card.pack(pady=(0, 20), fill="x")
        
        week_header = ctk.CTkFrame(week_card, fg_color="transparent")
        week_header.pack(fill="x", padx=20, pady=(20, 10))
        
        lbl_week = ctk.CTkLabel(
            week_header, text=self.app.lang.t("week_forecast"), 
            font=FONTS["section_head"], text_color=COLORS["text_primary"]
        )
        lbl_week.pack(side="left")
        
        self.btn_export = ctk.CTkButton(
            week_header, text=self.app.lang.t("export_btn"), width=80, height=28,
            fg_color=COLORS["bg_page"], text_color=COLORS["text_primary"],
            hover_color=COLORS["menu_item_hover"], font=FONTS["btn_text"],
            command=self.app.show_export_dialog
        )
        self.btn_export.pack(side="right")

        self.week_container = ctk.CTkFrame(week_card, fg_color="transparent")
        self.week_container.pack(fill="x", padx=20, pady=(0, 20))
        
        self.weekly_rows = []
        for _ in range(7):
            row = WeeklyRow(self.week_container)
            row.pack(fill="x", pady=5)
            self.weekly_rows.append(row)

        # Bind mouse wheel for all children
        self._bind_mouse_scroll(self.container)

    def _bind_mouse_scroll(self, widget):
        # On Windows/Linux, bind <MouseWheel> and <Button-4/5> to parent canvas
        def _scroll_handler(e):
            if hasattr(self.scroll_frame, '_parent_canvas'):
                canvas = self.scroll_frame._parent_canvas
                if e.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif e.num == 5:
                    canvas.yview_scroll(1, "units")
                else:
                    canvas.yview_scroll(int(-1*(e.delta/120)), "units")
                    
        widget.bind("<MouseWheel>", _scroll_handler, add="+")
        widget.bind("<Button-4>", _scroll_handler, add="+")
        widget.bind("<Button-5>", _scroll_handler, add="+")
        for child in widget.winfo_children():
            self._bind_mouse_scroll(child)

    def _on_search(self):
        query = self.search_entry.get().strip()
        if query:
            self.app.load_weather(query)

    def update_view(self, current, weekly, hourly):
        if current:
            self.current_city_data = current
            self.main_card.update_data(
                current['name'],
                datetime.datetime.now().strftime("%A, %B %d, %Y"),
                current['temp'],
                self.app.settings.get('temp_unit', 'C'),
                self.app.lang.t(f"conditions.{current['condition']}"),
                f"{self.app.lang.t('feels_like')} {int(current['feels_like'])}°C",
                current['icon_code']
            )

            self.t_hum.update_data(self.app.lang.t("humidity"), f"{int(current['humidity'])}%")
            self.t_wind.update_data(self.app.lang.t("wind_speed"), f"{int(current['wind_speed'])} km/h")
            self.t_vis.update_data(self.app.lang.t("visibility"), f"{int(current['visibility'])} km")
            self.t_pres.update_data(self.app.lang.t("pressure"), f"{current['pressure']} mb")
            self.t_dew.update_data(self.app.lang.t("dew_point"), f"{int(current['dew_point'])}°C")
            self.t_uv.update_data(self.app.lang.t("uv_index"), f"{current['uv_index']}")

        if hourly:
            self.hourly_chart.update_data(hourly)

        if weekly:
            for i, day_data in enumerate(weekly):
                if i < len(self.weekly_rows):
                    self.weekly_rows[i].update_data(
                        self.app.lang.t(f"days.{day_data['day_name']}"),
                        day_data['icon_code'],
                        self.app.lang.t(f"conditions.{day_data['condition']}"),
                        day_data['temp_min'],
                        day_data['temp_max'],
                        self.app.settings.get('temp_unit', 'C')
                    )

    def refresh_texts(self):
        self.search_entry.configure(placeholder_text=self.app.lang.t("search_placeholder"))
        self.btn_search.configure(text=self.app.lang.t("search_btn"))
        self.btn_export.configure(text=self.app.lang.t("export_btn"))
        self.lbl_subtitle.configure(text=self.app.lang.t("app_subtitle"))
