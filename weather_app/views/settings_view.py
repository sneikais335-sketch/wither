import customtkinter as ctk
import os
from PIL import Image
from config import COLORS, FONTS, ICONS
from database.settings_db import SettingsDB

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_page"], **kwargs)
        self.app = app_controller
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

        self.container = ctk.CTkFrame(self, width=900, fg_color="transparent")
        self.container.place(relx=0.5, rely=0, anchor="n", relheight=1)
        self.container.pack_propagate(False)

        self._build_header()
        self._build_settings()

    def _build_header(self):
        header = ctk.CTkFrame(self.container, width=900, height=120, fg_color="transparent")
        header.pack(pady=(40, 20))
        header.pack_propagate(False)

        self.btn_back = ctk.CTkButton(
            header, text=self.app.lang.t("back"), width=60, fg_color="transparent", 
            text_color=COLORS["text_primary"], font=FONTS["btn_text"],
            hover_color=COLORS["menu_item_hover"], command=lambda: self.app.show_view("main")
        )
        self.btn_back.place(x=0, rely=0.1)

        self.lbl_title = ctk.CTkLabel(
            header, text=self.app.lang.t("settings"), 
            text_color=COLORS["accent_blue"], font=("Segoe UI", 36, "bold")
        )
        self.lbl_title.pack()

        self.lbl_subtitle = ctk.CTkLabel(
            header, text=self.app.lang.t("settings_sub"), 
            text_color=COLORS["text_secondary"], font=("Segoe UI", 13)
        )
        self.lbl_subtitle.pack()

    def _build_settings(self):
        self.scroll = ctk.CTkScrollableFrame(
            self.container, width=750, height=600, fg_color="transparent",
            scrollbar_button_color=COLORS["menu_item_hover"],
            scrollbar_button_hover_color=COLORS["bg_card"],
            scrollbar_fg_color=COLORS["text_secondary"]
        )
        self.scroll.pack(pady=10, expand=True, fill="both")

        # 1. Display Section
        self.lbl_display = self._add_section_title(self.app.lang.t("display"))
        
        display_card = ctk.CTkFrame(self.scroll, fg_color=COLORS["bg_card"], corner_radius=20)
        display_card.pack(fill="x", pady=(0, 25), padx=20)
        
        self.sw_unit, self.lbl_unit_title, self.lbl_unit_sub = self._create_row(
            display_card, "sun.png", self.app.lang.t("temp_unit"), 
            self.app.lang.t("unit_desc"), 
            self._toggle_unit, is_switch=True
        )
        
        # Initial state for unit
        if self.app.settings.get('temp_unit') == 'F':
            self.sw_unit.select()

        # 2. Notifications Section
        self.lbl_notif = self._add_section_title(self.app.lang.t("notifications"))
        
        notif_card = ctk.CTkFrame(self.scroll, fg_color=COLORS["bg_card"], corner_radius=20)
        notif_card.pack(fill="x", pady=(0, 25), padx=20)
        
        self.sw_notif, self.lbl_notif_title, self.lbl_notif_sub = self._create_row(
            notif_card, "bell.png", self.app.lang.t("weather_alerts"), 
            self.app.lang.t("alert_desc"), 
            self._toggle_notif, is_switch=True
        )
        
        if self.app.settings.get('notifications_enabled'):
            self.sw_notif.select()

        # 3. Location Section
        self.lbl_loc = self._add_section_title(self.app.lang.t("location"))
        
        loc_card = ctk.CTkFrame(self.scroll, fg_color=COLORS["bg_card"], corner_radius=20)
        loc_card.pack(fill="x", pady=(0, 25), padx=20)
        
        self.sw_loc, self.lbl_loc_title, self.lbl_loc_sub = self._create_row(
            loc_card, "location.png", self.app.lang.t("auto_location"), 
            self.app.lang.t("loc_desc"), 
            self._toggle_loc, is_switch=True
        )
        
        if self.app.settings.get('auto_location'):
            self.sw_loc.select()

    def _add_section_title(self, title):
        lbl = ctk.CTkLabel(
            self.scroll, text=title, font=("Segoe UI", 16, "bold"), 
            text_color=COLORS["text_primary"], anchor="w"
        )
        lbl.pack(fill="x", padx=35, pady=(10, 5))
        return lbl

    def _create_row(self, parent, icon_file, title, subtitle, command, is_switch=True):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        row.pack(fill="x", padx=20, pady=5)
        row.pack_propagate(False)

        # Icon
        img = self._get_image(icon_file, (24, 24))
        icon_lbl = ctk.CTkLabel(row, image=img, text="", width=40)
        icon_lbl.pack(side="left", padx=(0, 15))

        # Text
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        
        lbl_title = ctk.CTkLabel(
            info, text=title, font=("Segoe UI", 15, "bold"), 
            text_color=COLORS["text_primary"], anchor="w"
        )
        lbl_title.pack(fill="x", pady=(15, 0))
        
        lbl_sub = ctk.CTkLabel(
            info, text=subtitle, font=("Segoe UI", 11), 
            text_color=COLORS["text_secondary"], anchor="w"
        )
        lbl_sub.pack(fill="x")

        # Control
        if is_switch:
            switch = ctk.CTkSwitch(
                row, text="", command=command, 
                progress_color="#3B82F6",
                button_color="#FFFFFF",
                button_hover_color="#F9FAFB",
                fg_color="#D1D5DB"
            )
            switch.pack(side="right", padx=10)
            return switch, lbl_title, lbl_sub
        
        return None, lbl_title, lbl_sub

    def _get_image(self, filename, size):
        path = os.path.join(self.assets_path, filename)
        if os.path.exists(path):
            return ctk.CTkImage(light_image=Image.open(path), size=size)
        return None

    def _toggle_unit(self):
        new_unit = "F" if self.sw_unit.get() else "C"
        SettingsDB.update_setting('temp_unit', new_unit)
        self.app.settings['temp_unit'] = new_unit
        # Force refresh of main view
        self.app.load_weather(self.app.current_city)

    def _toggle_notif(self):
        val = 1 if self.sw_notif.get() else 0
        SettingsDB.update_setting('notifications_enabled', val)
        self.app.settings['notifications_enabled'] = val

    def _toggle_loc(self):
        val = 1 if self.sw_loc.get() else 0
        SettingsDB.update_setting('auto_location', val)
        self.app.settings['auto_location'] = val

    def refresh_texts(self):
        self.btn_back.configure(text=self.app.lang.t("back"))
        self.lbl_title.configure(text=self.app.lang.t("settings"))
        self.lbl_subtitle.configure(text=self.app.lang.t("settings_sub"))
        
        self.lbl_display.configure(text=self.app.lang.t("display"))
        self.lbl_unit_title.configure(text=self.app.lang.t("temp_unit"))
        self.lbl_unit_sub.configure(text=self.app.lang.t("unit_desc"))
        
        self.lbl_notif.configure(text=self.app.lang.t("notifications"))
        self.lbl_notif_title.configure(text=self.app.lang.t("weather_alerts"))
        self.lbl_notif_sub.configure(text=self.app.lang.t("alert_desc"))
        
        self.lbl_loc.configure(text=self.app.lang.t("location"))
        self.lbl_loc_title.configure(text=self.app.lang.t("auto_location"))
        self.lbl_loc_sub.configure(text=self.app.lang.t("loc_desc"))
