import customtkinter as ctk
from config import COLORS, FONTS, SIZES

class StatTile(ctk.CTkFrame):
    def __init__(self, master, icon_color, icon_emoji, label_text, value_text, **kwargs):
        super().__init__(
            master, 
            width=SIZES["stat_tile_w"], 
            height=SIZES["stat_tile_h"], 
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            **kwargs
        )
        self.pack_propagate(False)

        # Icon box
        self.icon_frame = ctk.CTkFrame(
            self, width=36, height=36,
            fg_color=icon_color, corner_radius=8
        )
        self.icon_frame.place(x=15, y=15)
        self.icon_frame.pack_propagate(False)
        
        self.icon_label = ctk.CTkLabel(
            self.icon_frame, text=icon_emoji, text_color="white", font=("Segoe UI", 16)
        )
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Label (Title)
        self.lbl_title = ctk.CTkLabel(
            self, text=label_text, text_color=COLORS["text_secondary"], font=("Segoe UI", 12)
        )
        self.lbl_title.place(x=15, y=60)

        # Value
        self.lbl_value = ctk.CTkLabel(
            self, text=value_text, text_color=COLORS["text_primary"], font=("Segoe UI", 16, "bold")
        )
        self.lbl_value.place(x=15, y=85)
        
        # Override height to fit everything nicely
        self.configure(height=120)

    def update_data(self, label_text, value_text):
        self.lbl_title.configure(text=label_text)
        self.lbl_value.configure(text=value_text)
