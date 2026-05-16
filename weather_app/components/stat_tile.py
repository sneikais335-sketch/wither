import customtkinter as ctk
from config import COLORS, FONTS, SIZES
from utils.icons import IconManager

class StatTile(ctk.CTkFrame):
    def __init__(self, master, icon_color, icon_file, label_text, value_text, **kwargs):
        super().__init__(
            master, 
            width=SIZES["stat_tile_w"], 
            height=120, 
            fg_color=COLORS["bg_card_light"],
            corner_radius=20,
            border_width=1,
            border_color=COLORS["menu_item_hover"],
            **kwargs
        )
        self.pack_propagate(False)

        # Icon box
        self.icon_frame = ctk.CTkFrame(
            self, width=40, height=40,
            fg_color=icon_color, corner_radius=10
        )
        self.icon_frame.place(x=15, y=15)
        self.icon_frame.pack_propagate(False)
        
        img = IconManager.get_local_icon(icon_file, (22, 22))
        self.icon_label = ctk.CTkLabel(
            self.icon_frame, image=img, text=""
        )
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Label (Title)
        self.lbl_title = ctk.CTkLabel(
            self, text=label_text, text_color=COLORS["text_secondary"], font=("Segoe UI", 12)
        )
        self.lbl_title.place(x=15, y=65)

        # Value
        self.lbl_value = ctk.CTkLabel(
            self, text=value_text, text_color=COLORS["text_primary"], font=("Segoe UI", 18, "bold")
        )
        self.lbl_value.place(x=15, y=88)

    def update_data(self, label_text, value_text):
        self.lbl_title.configure(text=label_text)
        self.lbl_value.configure(text=value_text)
