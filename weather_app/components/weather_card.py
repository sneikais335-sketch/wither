import customtkinter as ctk
from config import COLORS, FONTS
from utils.icons import IconManager

class WeatherCard(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(
            master, 
            width=900,
            height=280, 
            fg_color="transparent",
            corner_radius=24,
            **kwargs
        )
        self.app = app_controller
        self.pack_propagate(False)

        # Draw Gradient Background
        from PIL import Image, ImageDraw
        def create_3_stop_gradient(w, h, c1="#99A1AF", c2="#6A7282", c3="#4A5565"):
            img = Image.new("RGB", (w, h))
            draw = ImageDraw.Draw(img)
            
            def hex_to_rgb(hx):
                hx = hx.lstrip('#')
                return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
                
            rgb1, rgb2, rgb3 = hex_to_rgb(c1), hex_to_rgb(c2), hex_to_rgb(c3)
            
            for y in range(h):
                if y < h / 2:
                    ratio = y / (h / 2)
                    r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
                    g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
                    b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)
                else:
                    ratio = (y - h / 2) / (h / 2)
                    r = int(rgb2[0] + (rgb3[0] - rgb2[0]) * ratio)
                    g = int(rgb2[1] + (rgb3[1] - rgb2[1]) * ratio)
                    b = int(rgb2[2] + (rgb3[2] - rgb2[2]) * ratio)
                draw.line([(0, y), (w, y)], fill=(r, g, b))
            return img

        grad_img = create_3_stop_gradient(900, 280)
        self.bg_image = ctk.CTkImage(light_image=grad_img, size=(900, 280))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="", corner_radius=24)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Soft icon background circle behind icon
        self.icon_bg = ctk.CTkFrame(
            self, width=190, height=190, fg_color="#FFFFFF", corner_radius=100
        )
        # Make it semi-transparent if possible, or just a solid color. User didn't specify. I'll leave it out since the design might not need it, or make it rgba. Actually, CTkFrame doesn't do alpha well, but we can do a hack. I'll just use #6A7282.
        self.icon_bg.configure(fg_color="#4A5565")
        self.icon_bg.place(relx=0.82, rely=0.55, anchor="center")
        self.icon_bg.pack_propagate(False)

        # Left side info
        self.city_label = ctk.CTkLabel(
            self, text="City Name", text_color=COLORS["text_white"], font=("Segoe UI", 28, "bold")
        )
        self.city_label.place(x=40, y=30)

        self.date_label = ctk.CTkLabel(
            self, text="Monday, 1 Jan", text_color="#E2E8F0", font=("Segoe UI", 12)
        )
        self.date_label.place(x=40, y=70)

        self.temp_label = ctk.CTkLabel(
            self, text="--", text_color=COLORS["text_white"], font=("Segoe UI", 80, "bold")
        )
        self.temp_label.place(x=40, y=100)
        
        self.unit_label = ctk.CTkLabel(
            self, text="°C", text_color=COLORS["text_white"], font=("Segoe UI", 40)
        )
        self.unit_label.place(x=150, y=120) # Dynamic in update_data

        self.condition_label = ctk.CTkLabel(
            self, text="--", text_color=COLORS["text_white"], font=("Segoe UI", 20)
        )
        self.condition_label.place(x=40, y=210)

        self.feels_like_label = ctk.CTkLabel(
            self, text="Feels like --", text_color="#E2E8F0", font=("Segoe UI", 12)
        )
        self.feels_like_label.place(x=40, y=240)

        self.icon_label = ctk.CTkLabel(
            self, text="", width=80, height=80
        )
        # Fixed absolute position on right side
        self.icon_label.place(x=700, y=100)

    def update_data(self, city, date_str, temp, unit, condition, feels_like, icon_code=""):
        self.city_label.configure(text=city)
        self.date_label.configure(text=date_str)
        self.temp_label.configure(text=f"{int(temp)}")
        
        # Adjust unit position based on temp length
        temp_len = len(str(int(temp)))
        x_offset = 40 + (temp_len * 45) + 10
        self.unit_label.place(x=x_offset, y=120)
        self.unit_label.configure(text=f"°{unit}")
        
        # Language updates will be registered in LanguageManager in the app
        # But we also translate condition and feels like here
        translated_cond = self.app.lang.t(f"conditions.{condition}") if self.app.lang.t(f"conditions.{condition}") != f"conditions.{condition}" else condition
        self.condition_label.configure(text=translated_cond)
        
        feels_text = self.app.lang.t("feels_like").replace("{temp}", f"{int(feels_like)}°{unit}")
        self.feels_like_label.configure(text=feels_text)

        # Load icon dynamically via icon_loader
        from utils.icon_loader import get_weather_icon
        img = get_weather_icon(icon_code, size=(80, 80), color="white")
            
        if img:
            self.icon_label.configure(image=img, text="")
        else:
            self.icon_label.configure(image="", text="Weather")
