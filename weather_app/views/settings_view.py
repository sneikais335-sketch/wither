import customtkinter as ctk
from config import COLORS, FONTS
from database.settings_db import SettingsDB

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_page"], **kwargs)
        self.app = app_controller

        self.container = ctk.CTkFrame(self, width=900, fg_color="transparent")
        self.container.place(relx=0.5, rely=0, anchor="n", relheight=1)
        self.container.pack_propagate(False)

        self._build_header()
        self._build_settings()

    def _build_header(self):
        header = ctk.CTkFrame(self.container, width=900, height=80, fg_color="transparent")
        header.pack(pady=(20, 30))
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        self.lbl_title = ctk.CTkLabel(title_frame, text=self.app.lang.t("settings"), text_color=COLORS["accent_blue"], font=FONTS["title_large"])
        self.lbl_title.pack()

        self.lbl_subtitle = ctk.CTkLabel(
            header, text="Customize your weather experience", 
            text_color=COLORS["text_secondary"], font=FONTS["subtitle"]
        )
        self.lbl_subtitle.place(relx=0.5, rely=0.8, anchor="center")

    def _build_settings(self):
        content = ctk.CTkFrame(self.container, width=700, fg_color="transparent")
        content.pack(pady=10)

        # 1. Display
        lbl_disp = ctk.CTkLabel(content, text="Display", font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"])
        lbl_disp.pack(anchor="w", padx=20, pady=(0, 5))
        
        card1 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=15)
        card1.pack(fill="x", pady=(0, 20))
        
        self._create_setting_row(card1, "🌡️", "Temperature Unit", "Choose between Celsius and Fahrenheit", self._toggle_unit, switch_text="°C / °F")
        self._create_setting_row(card1, "☀️", "Dark Mode", "Toggle dark theme (Coming Soon)", None, disabled=True)

        # 2. Notifications
        lbl_notif = ctk.CTkLabel(content, text="Notifications", font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"])
        lbl_notif.pack(anchor="w", padx=20, pady=(0, 5))
        
        card2 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=15)
        card2.pack(fill="x", pady=(0, 20))
        
        self.sw_alerts = self._create_setting_row(card2, "🔔", "Weather Alerts", "Get notified about severe weather", self._toggle_alerts)

        # 3. Location
        lbl_loc = ctk.CTkLabel(content, text="Location", font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"])
        lbl_loc.pack(anchor="w", padx=20, pady=(0, 5))
        
        card3 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=15)
        card3.pack(fill="x", pady=(0, 20))
        
        self.sw_loc = self._create_setting_row(card3, "📍", "Auto-detect Location", "Automatically detect your current location", self._toggle_location)
        
        # 4. Language (Extra)
        lbl_lang = ctk.CTkLabel(content, text="Language", font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"])
        lbl_lang.pack(anchor="w", padx=20, pady=(0, 5))
        
        card4 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=15)
        card4.pack(fill="x", pady=(0, 20))
        
        lang_frame = ctk.CTkFrame(card4, fg_color="transparent", height=60)
        lang_frame.pack(fill="x", padx=15, pady=10)
        lang_frame.pack_propagate(False)
        
        ctk.CTkLabel(lang_frame, text="🌐", font=("Segoe UI", 24)).pack(side="left", padx=(0, 15))
        info = ctk.CTkFrame(lang_frame, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(info, text="Language", font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"], anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text="Select your preferred language", font=("Segoe UI", 10), text_color=COLORS["text_secondary"], anchor="w").pack(fill="x")
        
        self.lang_var = ctk.StringVar(value=self.app.settings.get('language', 'en'))
        self.lang_menu = ctk.CTkOptionMenu(
            lang_frame, values=["en", "ru", "kg"], variable=self.lang_var,
            command=self._change_lang, width=80
        )
        self.lang_menu.pack(side="right")

        # Set initial states
        if self.app.settings.get('notifications'):
            self.sw_alerts.select()
        if self.app.settings.get('auto_location'):
            self.sw_loc.select()

    def _create_setting_row(self, parent, icon, title, subtitle, command, switch_text="", disabled=False):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        row.pack(fill="x", padx=15, pady=10)
        row.pack_propagate(False)

        # Icon
        icon_lbl = ctk.CTkLabel(row, text=icon, font=("Segoe UI", 24))
        icon_lbl.pack(side="left", padx=(0, 15))

        # Text
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(info, text=title, font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"], anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=subtitle, font=("Segoe UI", 10), text_color=COLORS["text_secondary"], anchor="w").pack(fill="x")

        # Control
        if switch_text:
            # Maybe a segmented button or a switch
            switch = ctk.CTkSwitch(row, text=switch_text, command=command)
        else:
            switch = ctk.CTkSwitch(row, text="", command=command)
            
        if disabled:
            switch.configure(state="disabled")
            
        switch.pack(side="right")
        return switch

    def _toggle_unit(self):
        # mock toggle
        pass

    def _toggle_alerts(self):
        SettingsDB.update_setting('notifications', self.sw_alerts.get())

    def _toggle_location(self):
        SettingsDB.update_setting('auto_location', self.sw_loc.get())

    def _change_lang(self, choice):
        self.app.switch_language(choice)

    def refresh_texts(self):
        self.lbl_title.configure(text=self.app.lang.t("settings"))
