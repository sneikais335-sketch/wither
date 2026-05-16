import customtkinter as ctk
from PIL import Image
import os
from config import COLORS, FONTS, ICONS

class MenuPanel(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(
            master, 
            width=320, 
            height=420, 
            fg_color="transparent",
            **kwargs
        )
        self.app = app_controller
        self.pack_propagate(False)

        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

        # Background Image
        bg_img = self._get_image("menu_bg_new.png", (320, 420))
        if bg_img:
            self.bg_lbl = ctk.CTkLabel(self, image=bg_img, text="")
            self.bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Content container
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=25)

        # 1. Header
        self.header = ctk.CTkFrame(self.content, height=110, fg_color="transparent")
        self.header.pack(fill="x", pady=(10, 0))
        self.header.pack_propagate(False)
        
        # Create gradient background
        from PIL import Image, ImageDraw
        def create_gradient(w, h, c1, c2):
            img = Image.new("RGB", (w, h))
            draw = ImageDraw.Draw(img)
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            for i in range(w):
                r = int(r1 + (r2 - r1) * i / w)
                g = int(g1 + (g2 - g1) * i / w)
                b = int(b1 + (b2 - b1) * i / w)
                draw.line([(i, 0), (i, h)], fill=(r, g, b))
            return img
            
        grad_img = create_gradient(280, 110, "#3B82F6", "#7C3AED")
        self.header_bg = ctk.CTkImage(light_image=grad_img, size=(280, 110))
        self.bg_label = ctk.CTkLabel(self.header, image=self.header_bg, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.lbl_menu = ctk.CTkLabel(self.header, text=self.app.lang.t("menu_title"), font=("Segoe UI", 22, "bold"), text_color="#FFFFFF")
        self.lbl_menu.pack(anchor="w", padx=25, pady=(25, 0))
        
        self.lbl_sub = ctk.CTkLabel(
            self.header, text=self.app.lang.t("menu_subtitle"), 
            font=("Segoe UI", 12), text_color="#E0E7FF"
        )
        self.lbl_sub.pack(anchor="w", padx=25, pady=(3, 0))

        # 2. Body area
        self.body = ctk.CTkFrame(self.content, fg_color="transparent")
        self.body.pack(fill="both", expand=True, pady=10)

        # Navigation buttons as cards
        self.btn_saved = self._create_nav_card(
            self.app.lang.t("saved_cities"), "saved_cities", "location.png", 
            COLORS["menu_icon_saved"], lambda: self._navigate("saved")
        )
        self.btn_settings = self._create_nav_card(
            self.app.lang.t("settings"), "settings", "settings.png", 
            COLORS["menu_icon_set"], lambda: self._navigate("settings")
        )

        # 3. Language Section
        div_img = self._get_image("menu_divider.png", (280, 2))
        if div_img:
            line = ctk.CTkLabel(self.content, image=div_img, text="")
            line.pack(fill="x", pady=5)
        else:
            line = ctk.CTkFrame(self.content, height=1, fg_color="#E2E8F0")
            line.pack(fill="x", pady=5)

        lang_header = ctk.CTkFrame(self.content, fg_color="transparent")
        lang_header.pack(fill="x", pady=(10, 5))
        
        globe_icon = self._get_image("globe.png", (18, 18))
        ctk.CTkLabel(lang_header, image=globe_icon, text="").pack(side="left")
        self.lbl_lang = ctk.CTkLabel(lang_header, text=self.app.lang.t("language"), font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"])
        self.lbl_lang.pack(side="left", padx=10)

        self.lang_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.lang_frame.pack(fill="x", pady=(0, 10))
        
        self.lang_btns = {}
        for code in ["EN", "RU", "KG"]:
            btn = ctk.CTkButton(
                self.lang_frame, text=code, width=70, height=35,
                fg_color="#F3F4F6", text_color=COLORS["text_primary"],
                hover_color="#E5E7EB", corner_radius=10,
                command=lambda c=code.lower(): self._change_lang(c)
            )
            btn.pack(side="left", padx=5, expand=True)
            self.lang_btns[code.lower()] = btn

        self.refresh_texts()

    def _get_image(self, filename, size):
        path = os.path.join(self.assets_path, filename)
        if os.path.exists(path):
            return ctk.CTkImage(light_image=Image.open(path), size=size)
        return None

    def _create_nav_card(self, text, key, icon_file, icon_bg, command):
        card = ctk.CTkFrame(self.body, fg_color=COLORS["bg_card_light"], height=70, corner_radius=20, border_width=1, border_color="#E6EEF9")
        card.pack(fill="x", pady=8)
        card.pack_propagate(False)
        
        icon_box = ctk.CTkFrame(card, width=50, height=50, fg_color=icon_bg, corner_radius=15)
        icon_box.place(x=15, y=10)
        icon_box.pack_propagate(False)
        
        img = self._get_image(icon_file, (22, 22))
        if img:
            ctk.CTkLabel(icon_box, image=img, text="").place(relx=0.5, rely=0.5, anchor="center")
        
        lbl = ctk.CTkLabel(card, text=text, font=("Segoe UI", 14, "bold"), text_color=COLORS["text_primary"])
        lbl.place(x=80, y=22)
        
        card.bind("<Button-1>", lambda e: command())
        lbl.bind("<Button-1>", lambda e: command())
        icon_box.bind("<Button-1>", lambda e: command())
        
        card.key = key
        card.lbl = lbl
        return card

    def _navigate(self, view_name):
        if view_name == "saved":
            self.app.views["main"].show_saved_cities()
            self.app.show_view("main")
        else:
            self.app.show_view(view_name)
        self.app.toggle_menu()

    def _change_lang(self, code):
        self.app.switch_language(code)
        self.refresh_texts()

    def refresh_texts(self):
        self.lbl_menu.configure(text=self.app.lang.t("menu_title"))
        self.lbl_sub.configure(text=self.app.lang.t("menu_subtitle"))
        
        self.btn_saved.lbl.configure(text=self.app.lang.t("saved_cities"))
        self.btn_settings.lbl.configure(text=self.app.lang.t("settings"))
        self.lbl_lang.configure(text=self.app.lang.t("language"))
        
        # Update language buttons highlighting
        current = self.app.lang.current
        for code, btn in self.lang_btns.items():
            if code == current:
                btn.configure(fg_color=COLORS["accent_blue"], text_color="white")
                # Add checkmark if possible or just color
                btn.configure(text=f"{code.upper()}  ✓")
            else:
                btn.configure(fg_color="#F3F4F6", text_color=COLORS["text_primary"], text=code.upper())
