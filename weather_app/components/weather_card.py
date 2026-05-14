import customtkinter as ctk
from config import COLORS, FONTS
from utils.icons import IconManager

class WeatherCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            width=900,
            height=280, 
            fg_color=COLORS["bg_main_card"],
            corner_radius=20,
            **kwargs
        )
        self.pack_propagate(False)

        # Left side info
        self.city_label = ctk.CTkLabel(
            self, text="City Name", text_color=COLORS["text_white"], font=("Segoe UI", 28)
        )
        self.city_label.place(x=40, y=30)

        self.date_label = ctk.CTkLabel(
            self, text="Monday, 1 Jan", text_color="#E2E8F0", font=("Segoe UI", 12)
        )
        self.date_label.place(x=40, y=70)

        self.temp_label = ctk.CTkLabel(
            self, text="--", text_color=COLORS["text_white"], font=("Segoe UI", 80)
        )
        self.temp_label.place(x=40, y=100)
        
        self.unit_label = ctk.CTkLabel(
            self, text="°C", text_color=COLORS["text_white"], font=("Segoe UI", 40)
        )
        self.unit_label.place(x=150, y=110) # Dynamic in update_data

        self.condition_label = ctk.CTkLabel(
            self, text="--", text_color=COLORS["text_white"], font=("Segoe UI", 20)
        )
        self.condition_label.place(x=40, y=210)

        self.feels_like_label = ctk.CTkLabel(
            self, text="Feels like --", text_color="#E2E8F0", font=("Segoe UI", 12)
        )
        self.feels_like_label.place(x=40, y=240)

        self.icon_label = ctk.CTkLabel(
            self, text="", width=150, height=150
        )
        self.icon_label.place(relx=0.85, rely=0.5, anchor="center")

    def update_data(self, city, date_str, temp, unit, condition, feels_like, icon_code=""):
        self.city_label.configure(text=city)
        self.date_label.configure(text=date_str)
        self.temp_label.configure(text=f"{int(temp)}")
        
        # Adjust unit position based on temp length
        temp_len = len(str(int(temp)))
        x_offset = 40 + (temp_len * 45) + 10
        self.unit_label.place(x=x_offset, y=120)
        self.unit_label.configure(text=f"°{unit}")
        
        self.condition_label.configure(text=condition)
        self.feels_like_label.configure(text=feels_like)

        # Load icon dynamically
        if icon_code:
            img = IconManager.get_icon(icon_code, size=(180, 180))
            if img:
                self.icon_label.configure(image=img)
            else:
                self.icon_label.configure(image="", text="☁️")
        else:
            self.icon_label.configure(image="", text="☁️")
