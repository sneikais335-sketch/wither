import customtkinter as ctk
from config import COLORS, FONTS
from utils.icons import IconManager

class WeeklyRow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            height=50, 
            fg_color="transparent",
            **kwargs
        )
        self.pack_propagate(False)

        # Left aligned elements
        self.day_label = ctk.CTkLabel(
            self, text="Day", width=120, anchor="w",
            text_color=COLORS["text_secondary"], font=("Segoe UI", 14)
        )
        self.day_label.pack(side="left", padx=(10, 20))

        self.icon_label = ctk.CTkLabel(self, text="☁️", width=30, font=("Segoe UI", 18))
        self.icon_label.pack(side="left")

        self.cond_label = ctk.CTkLabel(
            self, text="Condition", width=150, anchor="w",
            text_color=COLORS["text_secondary"], font=("Segoe UI", 14)
        )
        self.cond_label.pack(side="left", padx=10)

        # Right aligned elements (packed right to left)
        self.max_temp_label = ctk.CTkLabel(
            self, text="--", width=40, anchor="e", text_color=COLORS["text_primary"], font=("Segoe UI", 14, "bold")
        )
        self.max_temp_label.pack(side="right", padx=(10, 10))

        # Bar representation using line with round caps
        self.bar_canvas = ctk.CTkCanvas(
            self, height=20, width=80, bg=COLORS["bg_card"], highlightthickness=0
        )
        self.bar_canvas.pack(side="right", padx=10, pady=15)

        self.min_temp_label = ctk.CTkLabel(
            self, text="--", width=40, anchor="w", text_color=COLORS["text_secondary"], font=("Segoe UI", 14)
        )
        self.min_temp_label.pack(side="right", padx=(10, 10))

    def update_data(self, day_name, icon, condition, temp_min, temp_max, unit_str):
        self.day_label.configure(text=day_name)
        self.cond_label.configure(text=condition)
        self.min_temp_label.configure(text=f"{int(temp_min)}°")
        self.max_temp_label.configure(text=f"{int(temp_max)}°")
        
        # Load icon
        img = IconManager.get_icon(icon, size=(30, 30))
        if img:
            self.icon_label.configure(image=img, text="")
        else:
            self.icon_label.configure(text="☁️", image="")

        # Update bar visualization
        self.bar_canvas.delete("all")
        # Base bar
        self.bar_canvas.create_line(5, 10, 75, 10, fill="#E2E8F0", width=6, capstyle="round")
        # Value bar (mocked position based on generic temps)
        self.bar_canvas.create_line(25, 10, 60, 10, fill=COLORS["temp_bar_hot"], width=6, capstyle="round")
