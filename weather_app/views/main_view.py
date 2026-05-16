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
        
        self.home_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.home_frame.pack(fill="both", expand=True)
        
        self._build_search(self.home_frame)
        self._build_content(self.home_frame)
        
        self.saved_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.empty_label = None

    def show_saved_cities(self):
        self.home_frame.pack_forget()
        self.saved_frame.pack(fill="both", expand=True, pady=20)
        self._load_saved_cities()

    def show_home(self):
        self.saved_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    def _load_saved_cities(self):
        for widget in self.saved_frame.winfo_children():
            widget.destroy()

        from database.cities_db import CitiesDB
        from components.city_card import CityCard
        cities = CitiesDB.get_all_cities()
        if not cities:
            self.empty_label = ctk.CTkLabel(
                self.saved_frame, 
                text=self.app.lang.t("no_cities") + "\n\n" + self.app.lang.t("no_cities_sub"),
                text_color=COLORS["text_secondary"], font=FONTS["subtitle"],
                justify="center"
            )
            self.empty_label.pack(pady=100)
            return

        row, col = 0, 0
        for city in cities:
            card = CityCard(
                self.saved_frame, 
                on_click_callback=self._on_saved_city_click,
                on_delete_callback=self._on_saved_city_delete
            )
            card.grid(row=row, column=col, padx=15, pady=15)
            
            card.update_data(city['id'], city['name'], 0, "Loading...", 0, 0, 0)
            current_data = self.app.fetch_current_weather_sync(city['name'])
            if current_data:
                card.update_data(
                    city['id'], city['name'], current_data['temp'], 
                    self.app.lang.t(f"conditions.{current_data['condition']}"), 
                    current_data['feels_like'], current_data['humidity'], current_data['wind_speed']
                )

            col += 1
            if col > 2: 
                col = 0
                row += 1

    def _on_saved_city_click(self, city_name):
        self.show_home()
        self.app.load_weather(city_name)

    def _on_saved_city_delete(self, city_id):
        from database.cities_db import CitiesDB
        CitiesDB.delete_city(city_id)
        self._load_saved_cities()

    def _build_header(self):
        header = ctk.CTkFrame(self.container, width=900, height=160, fg_color=COLORS["bg_card_light"], corner_radius=30)
        header.pack(pady=(0, 20), fill="x")
        header.pack_propagate(False)

        # Menu button (left)
        self.btn_menu = ctk.CTkButton(
            header, text="☰", width=50, height=50, font=("Segoe UI", 24),
            fg_color=COLORS["bg_card"], text_color=COLORS["text_primary"],
            corner_radius=18, command=self.app.toggle_menu
        )
        self.btn_menu.place(x=20, rely=0.28, anchor="w")

        # Titles (centered)
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.28, anchor="center")
        
        self.lbl_title_w = ctk.CTkLabel(title_frame, text="Weather", text_color=COLORS["accent_blue"], font=FONTS["title_large"])
        self.lbl_title_w.pack(side="left")
        
        self.lbl_title_f = ctk.CTkLabel(title_frame, text=" Forecast", text_color=COLORS["accent_purple"], font=FONTS["title_large"])
        self.lbl_title_f.pack(side="left")

        self.lbl_subtitle = ctk.CTkLabel(
            header, text=self.app.lang.t("app_subtitle"), 
            text_color=COLORS["text_secondary"], font=FONTS["subtitle"]
        )
        self.lbl_subtitle.place(relx=0.5, rely=0.62, anchor="center")

        # Calendar trigger (right)
        from utils.icons import IconManager
        cal_img = IconManager.get_local_icon("calendar.png", size=(24, 24))
        
        self.btn_calendar = ctk.CTkButton(
            header, text=" " + datetime.datetime.now().strftime("%d.%m.%Y"), image=cal_img,
            width=140, height=40,
            fg_color=COLORS["bg_card"], text_color=COLORS["text_primary"],
            font=FONTS["btn_text"], hover_color=COLORS["menu_item_hover"],
            corner_radius=20, command=self.app.show_calendar
        )
        self.btn_calendar.place(relx=0.98, rely=0.28, anchor="e")

    def _quick_search(self, city):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, city)
        self._on_search()

    def _build_search(self, parent):
        self.search_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.search_container.pack(pady=(0, 25), fill="x")

        # White pill block
        pill = ctk.CTkFrame(self.search_container, height=50, fg_color=COLORS["bg_card"], corner_radius=25)
        pill.pack(pady=(0, 8))
        
        from utils.icon_loader import load_icon
        
        # Magnifier icon
        icon_mag = load_icon("Vector-2.png", (16, 16), "gray")
        if not icon_mag:
            lbl_icon = ctk.CTkLabel(pill, text="🔍", text_color="#9CA3AF", font=("Segoe UI", 16))
        else:
            lbl_icon = ctk.CTkLabel(pill, image=icon_mag, text="")
        lbl_icon.pack(side="left", padx=(20, 8))

        self.search_entry = ctk.CTkEntry(
            pill, width=320, height=40, placeholder_text=self.app.lang.t("search_placeholder"),
            font=FONTS["search_input"], fg_color=COLORS["bg_card"], text_color=COLORS["text_primary"],
            border_width=0
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self._on_search())

        # Save Button
        icon_heart = load_icon("Vector-1.png", (16, 16), "original") # using "original" or "white"? Wait, user said "иконка сердца из SVG icons зелёного цвета слева" -> maybe "original" is already green, if not we don't have green color in loader. I'll pass "original".
        # User: "текст «Save» зелёного цвета #22C55E, corner_radius 20 (pill-форма), высота 36 пикселей. Обводка зелёного цвета #22C55E толщиной 1.5px"
        self.btn_save_city = ctk.CTkButton(
            pill, text="Save", image=icon_heart, width=80, height=36,
            fg_color="transparent", text_color="#22C55E", border_color="#22C55E", border_width=2,
            corner_radius=20, hover_color="#DCFCE7", command=self._save_current_city
        )
        self.btn_save_city.pack(side="left", padx=(0, 10))
        self.btn_save_city.configure(state="disabled") # Disabled initially

        self.btn_search = ctk.CTkButton(
            pill, text=self.app.lang.t("search_btn"), width=120, height=50,
            font=FONTS["btn_text"], fg_color="#111827", text_color=COLORS["text_white"],
            corner_radius=8, hover_color="#1F2937", command=self._on_search
        )
        self.btn_search.pack(side="left")
        
        # Popular Cities Bar
        pop_frame = ctk.CTkFrame(self.search_container, fg_color="transparent")
        pop_frame.pack()
        
        icon_loc = load_icon("location.png", (14, 14), "gray")
        lbl_pop_icon = ctk.CTkLabel(pop_frame, image=icon_loc, text="")
        lbl_pop_icon.pack(side="left", padx=(0, 5))
        
        lbl_pop = ctk.CTkLabel(pop_frame, text="Popular: ", text_color="#6B7280", font=("Segoe UI", 12))
        lbl_pop.pack(side="left")
        
        cities = ["San Francisco", "New York", "London", "Tokyo", "Paris"]
        for i, city in enumerate(cities):
            btn = ctk.CTkButton(
                pop_frame, text=city, width=0, height=20,
                fg_color="transparent", text_color="#3B82F6", hover_color=COLORS["menu_item_hover"],
                font=("Segoe UI", 12), cursor="hand2",
                command=lambda c=city: self._quick_search(c)
            )
            btn.pack(side="left")
            if i < len(cities) - 1:
                sep = ctk.CTkLabel(pop_frame, text=" · ", text_color="#6B7280", font=("Segoe UI", 12))
                sep.pack(side="left")

    def _save_current_city(self):
        query = self.search_entry.get().strip()
        if query:
            self.app.save_city(query)
            self._show_toast("✓ Город сохранён")

    def _show_toast(self, message):
        toast = ctk.CTkFrame(self.container, fg_color="#22C55E", corner_radius=20)
        toast.place(relx=0.5, rely=0.9, anchor="center")
        lbl = ctk.CTkLabel(toast, text=message, text_color="white", font=("Segoe UI", 14, "bold"))
        lbl.pack(padx=20, pady=10)
        self.after(2000, toast.destroy)

    def _build_content(self, parent):
        # Main Card
        self.main_card = WeatherCard(parent)
        self.main_card.pack(pady=(0, 20))

        # Stat Tiles row
        self.tiles_frame = ctk.CTkFrame(parent, width=900, height=120, fg_color="transparent")
        self.tiles_frame.pack(pady=(0, 20))
        self.tiles_frame.pack_propagate(False)
        
        # We need to distribute 6 tiles evenly
        # 6 * 130 = 780. 900 - 780 = 120 / 5 = 24px gap
        
        self.t_hum = StatTile(self.tiles_frame, COLORS["icon_humidity"], "humidity.png", self.app.lang.t("humidity"), "--%")
        self.t_hum.pack(side="left")
        
        self.t_wind = StatTile(self.tiles_frame, COLORS["icon_wind"], "wind.png", self.app.lang.t("wind_speed"), "--")
        self.t_wind.pack(side="left", padx=(24, 0))
        
        self.t_vis = StatTile(self.tiles_frame, COLORS["icon_visibility"], "visibility.png", self.app.lang.t("visibility"), "--")
        self.t_vis.pack(side="left", padx=(24, 0))
        
        self.t_pres = StatTile(self.tiles_frame, COLORS["icon_pressure"], "pressure.png", self.app.lang.t("pressure"), "--")
        self.t_pres.pack(side="left", padx=(24, 0))
        
        self.t_dew = StatTile(self.tiles_frame, COLORS["icon_dew"], "dew_point.png", self.app.lang.t("dew_point"), "--")
        self.t_dew.pack(side="left", padx=(24, 0))
        
        self.t_uv = StatTile(self.tiles_frame, COLORS["icon_uv"], "uv_index.png", self.app.lang.t("uv_index"), "--")
        self.t_uv.pack(side="left", padx=(24, 0))

        # Today's Temperature Card
        today_card = ctk.CTkFrame(parent, width=900, height=260, fg_color=COLORS["bg_card_light"], corner_radius=30)
        today_card.pack(pady=(0, 20), fill="x")
        today_card.pack_propagate(False)
        
        lbl_today = ctk.CTkLabel(
            today_card, text=self.app.lang.t("today_temp"), 
            font=FONTS["section_head"], text_color=COLORS["text_primary"]
        )
        lbl_today.pack(anchor="w", padx=20, pady=(20, 10))

        self.hourly_chart = HourlyChart(today_card)
        self.hourly_chart.pack(fill="x", padx=20, pady=(0, 20))

        # 7-Day Forecast Card
        week_card = ctk.CTkFrame(parent, width=900, height=650, fg_color=COLORS["bg_card_light"], corner_radius=30)
        week_card.pack(pady=(0, 20), fill="x")
        week_card.pack_propagate(False)
        
        week_header = ctk.CTkFrame(week_card, fg_color="transparent")
        week_header.pack(fill="x", padx=20, pady=(20, 10))
        
        lbl_week = ctk.CTkLabel(
            week_header, text=self.app.lang.t("week_forecast"), 
            font=FONTS["section_head"], text_color=COLORS["text_primary"]
        )
        lbl_week.pack(side="left")
        
        # Export Button
        self.btn_export = ctk.CTkButton(
            week_header, text=self.app.lang.t("export_btn") + " ▾", width=110, height=34,
            fg_color=COLORS["accent_blue"], text_color=COLORS["text_white"],
            hover_color="#3b6be0", font=("Segoe UI", 13, "bold"),
            corner_radius=17, command=self._toggle_export_dropdown
        )
        self.btn_export.pack(side="right")
        
        # Export Dropdown Frame (Hidden by default)
        self.export_dropdown = ctk.CTkFrame(
            self.container, width=120, fg_color=COLORS["bg_card"],
            corner_radius=10, border_width=1, border_color=COLORS["menu_item_hover"]
        )
        # Add buttons to dropdown
        ctk.CTkButton(self.export_dropdown, text="JSON", fg_color="transparent", text_color=COLORS["text_primary"], command=lambda: self._export_format("json")).pack(fill="x", pady=2, padx=5)
        ctk.CTkButton(self.export_dropdown, text="CSV", fg_color="transparent", text_color=COLORS["text_primary"], command=lambda: self._export_format("csv")).pack(fill="x", pady=2, padx=5)
        ctk.CTkButton(self.export_dropdown, text="Excel (.xlsx)", fg_color="transparent", text_color=COLORS["text_primary"], command=lambda: self._export_format("excel")).pack(fill="x", pady=2, padx=5)
        
        # Bind click elsewhere to hide
        self.container.bind("<Button-1>", self._hide_export_dropdown, add="+")

        self.week_container = ctk.CTkFrame(week_card, fg_color="transparent")
        self.week_container.pack(fill="x", padx=20, pady=(0, 20))
        
        self.weekly_rows = []
        for _ in range(7):
            row = WeeklyRow(self.week_container)
            row.pack(fill="x", pady=6)
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

    def _toggle_export_dropdown(self):
        if self.export_dropdown.winfo_ismapped():
            self.export_dropdown.place_forget()
        else:
            # Place it just below the button. The button is packed in week_header, which is in week_card
            x = self.btn_export.winfo_rootx() - self.container.winfo_rootx()
            y = self.btn_export.winfo_rooty() - self.container.winfo_rooty() + self.btn_export.winfo_height()
            self.export_dropdown.place(x=x, y=y)
            self.export_dropdown.lift()

    def _hide_export_dropdown(self, event=None):
        if hasattr(self, 'export_dropdown') and self.export_dropdown.winfo_ismapped():
            # Check if clicked inside dropdown
            if event:
                x, y = event.x_root, event.y_root
                x1 = self.export_dropdown.winfo_rootx()
                y1 = self.export_dropdown.winfo_rooty()
                x2 = x1 + self.export_dropdown.winfo_width()
                y2 = y1 + self.export_dropdown.winfo_height()
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return # Clicked inside dropdown
                # Check if clicked on button itself to avoid immediate re-hide
                bx1 = self.btn_export.winfo_rootx()
                by1 = self.btn_export.winfo_rooty()
                bx2 = bx1 + self.btn_export.winfo_width()
                by2 = by1 + self.btn_export.winfo_height()
                if bx1 <= x <= bx2 and by1 <= y <= by2:
                    return
            self.export_dropdown.place_forget()

    def _export_format(self, fmt):
        self.export_dropdown.place_forget()
        from components.export_dialog import ExportDialog
        # Just instantiate dialog silently and call export format directly!
        dialog = ExportDialog(self.app, self.app)
        dialog.withdraw() # hide it
        if fmt == "json":
            dialog._export_json()
        elif fmt == "csv":
            dialog._export_csv()
        elif fmt == "excel":
            dialog._export_excel()

    def _on_search(self):
        query = self.search_entry.get().strip()
        if query:
            self.app.load_weather(query)
            self.btn_save_city.configure(state="normal")

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
            self.t_uv.update_data(self.app.lang.t("uv_index"), str(current.get('uv_index', 0)))

        if hourly:
            self.hourly_chart.update_data(hourly)

        if weekly:
            temps_min = [d['temp_min'] for d in weekly]
            temps_max = [d['temp_max'] for d in weekly]
            week_min = min(temps_min) if temps_min else 0
            week_max = max(temps_max) if temps_max else 1

            for i, row in enumerate(self.weekly_rows):
                if i < len(weekly):
                    day_data = weekly[i]
                    row.update_data(
                        self.app.lang.t(f"days.{day_data['day_name']}"),
                        day_data['icon_code'],
                        self.app.lang.t(f"conditions.{day_data['condition']}"),
                        day_data['temp_min'],
                        day_data['temp_max'],
                        self.app.settings.get('temp_unit', 'C'),
                        week_min,
                        week_max
                    )
                    row.pack(fill="x", pady=6)
                else:
                    row.pack_forget()

    def refresh_texts(self):
        self.search_entry.configure(placeholder_text=self.app.lang.t("search_placeholder"))
        self.search_entry.bind("<Return>", lambda e: self._on_search())
        self.btn_search.configure(text=self.app.lang.t("search_btn"))
        self.btn_export.configure(text=self.app.lang.t("export_btn"))
        self.lbl_subtitle.configure(text=self.app.lang.t("app_subtitle"))
