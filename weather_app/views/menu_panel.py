import customtkinter as ctk
from config import COLORS, FONTS

class MenuPanel(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(
            master, 
            width=260, 
            height=200, 
            fg_color=COLORS["bg_card"],
            corner_radius=20,
            **kwargs
        )
        self.app = app_controller
        self.pack_propagate(False)

        # Header area with purple gradient-like background
        self.header = ctk.CTkFrame(self, height=70, fg_color=COLORS["accent_purple"], corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        lbl_menu = ctk.CTkLabel(self.header, text="Menu", font=("Segoe UI", 18, "bold"), text_color="white")
        lbl_menu.pack(anchor="w", padx=20, pady=(15, 0))
        
        lbl_sub = ctk.CTkLabel(self.header, text="Manage your weather preferences", font=("Segoe UI", 10), text_color="#E2E8F0")
        lbl_sub.pack(anchor="w", padx=20)

        # Body area
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, pady=10)

        # Navigation items
        self.nav_buttons = []
        
        self.btn_saved = self._create_nav_btn("📍", "saved_cities", lambda: self._navigate("saved"))
        self.btn_settings = self._create_nav_btn("⚙️", "settings", lambda: self._navigate("settings"))
        
        # We can also add a language switcher here or it can stay in settings. Let's keep it in menu.
        # But wait, Group 7.png only shows Saved Cities and Settings. So I will omit Language or keep it minimal.
        
        self.refresh_texts()

    def _create_nav_btn(self, icon, text_key, command):
        btn = ctk.CTkButton(
            self.body,
            text="",
            height=40,
            fg_color="transparent",
            text_color=COLORS["text_primary"],
            hover_color=COLORS["menu_item_hover"],
            anchor="w",
            command=command
        )
        btn.pack(fill="x", padx=10, pady=2)
        
        # Store icon and key for dynamic text update
        btn.icon = icon
        btn.text_key = text_key
        
        self.nav_buttons.append(btn)
        return btn

    def _navigate(self, view_name):
        self.app.show_view(view_name)
        self.app.toggle_menu() # close menu

    def refresh_texts(self):
        for btn in self.nav_buttons:
            text = self.app.lang.t(btn.text_key)
            btn.configure(text=f"  {btn.icon}   {text}")
