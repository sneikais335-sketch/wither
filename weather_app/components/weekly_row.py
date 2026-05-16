import customtkinter as ctk
from config import COLORS, FONTS
from utils.icons import IconManager

class WeeklyRow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            height=70, 
            fg_color=COLORS["bg_card_light"],
            corner_radius=20,
            border_width=1,
            border_color=COLORS["menu_item_hover"],
            **kwargs
        )
        self.pack_propagate(False)

        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.pack(side="left", fill="y", padx=(10, 10), pady=10)

        self.day_label = ctk.CTkLabel(
            self.left_frame, text="Day", anchor="w",
            text_color=COLORS["text_secondary"], font=("Segoe UI", 14)
        )
        self.day_label.pack(anchor="w")

        self.cond_label = ctk.CTkLabel(
            self.left_frame, text="Condition",
            text_color=COLORS["text_secondary"], font=("Segoe UI", 12)
        )
        self.cond_label.pack(anchor="w", pady=(4, 0))

        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.pack(side="left", fill="both", expand=True)

        self.icon_label = ctk.CTkLabel(self.center_frame, text="☁️", width=30, font=("Segoe UI", 18))
        self.icon_label.pack(side="left", padx=(0, 10))

        self.bar_canvas = ctk.CTkCanvas(
            self.center_frame, height=20, width=120, bg=COLORS["bg_card_light"], highlightthickness=0
        )
        self.bar_canvas.pack(side="left", padx=(0, 10), pady=10)

        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.pack(side="right", fill="y", padx=(10, 15), pady=10)

        self.max_temp_label = ctk.CTkLabel(
            self.right_frame, text="--", anchor="e", text_color=COLORS["text_primary"], font=("Segoe UI", 14, "bold")
        )
        self.max_temp_label.pack(anchor="e")

        self.min_temp_label = ctk.CTkLabel(
            self.right_frame, text="--", anchor="e", text_color=COLORS["text_secondary"], font=("Segoe UI", 12)
        )
        self.min_temp_label.pack(anchor="e", pady=(6, 0))

    def update_data(self, day_name, icon, condition, temp_min, temp_max, unit_str, week_min=0, week_max=1):
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
        self.bar_canvas.create_line(5, 10, 115, 10, fill="#E2E8F0", width=4, capstyle="round")
        
        # Value bar scaled by week's min/max
        week_range = max(1, week_max - week_min)
        start_ratio = max(0, min(1, (temp_min - week_min) / week_range))
        end_ratio = max(0, min(1, (temp_max - week_min) / week_range))
        
        start_x = 5 + int(110 * start_ratio)
        end_x = 5 + int(110 * end_ratio)
        if end_x <= start_x: end_x = start_x + 1
        
        mid_x = (start_x + end_x) // 2
        
        # Two-color bar
        self.bar_canvas.create_line(start_x, 10, mid_x, 10, fill="#86EFAC", width=4, capstyle="round")
        self.bar_canvas.create_line(mid_x, 10, end_x, 10, fill="#FDE047", width=4, capstyle="round")
