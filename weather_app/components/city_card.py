import customtkinter as ctk
from config import COLORS, FONTS, SIZES

class CityCard(ctk.CTkFrame):
    def __init__(self, master, on_click_callback=None, on_delete_callback=None, **kwargs):
        super().__init__(
            master, 
            width=SIZES["city_card_w"], 
            height=SIZES["city_card_h"], 
            fg_color=COLORS["city_card_bg"],
            corner_radius=15,
            **kwargs
        )
        self.pack_propagate(False)
        self.on_click_callback = on_click_callback
        self.on_delete_callback = on_delete_callback

        self.bind("<Button-1>", self._on_click)

        # Content
        self.city_label = ctk.CTkLabel(
            self, text="City", text_color=COLORS["text_white"], font=FONTS["city_name"]
        )
        self.city_label.place(x=15, y=10)
        self.city_label.bind("<Button-1>", self._on_click)

        self.temp_label = ctk.CTkLabel(
            self, text="--°", text_color=COLORS["text_white"], font=("Segoe UI", 32, "bold")
        )
        self.temp_label.place(x=15, y=45)
        self.temp_label.bind("<Button-1>", self._on_click)
        
        self.cond_label = ctk.CTkLabel(
            self, text="--", text_color=COLORS["text_white"], font=FONTS["condition"]
        )
        self.cond_label.place(x=80, y=55)
        self.cond_label.bind("<Button-1>", self._on_click)

        # Delete button
        self.btn_delete = ctk.CTkButton(
            self, text="✕", width=30, height=30, fg_color="transparent", 
            text_color=COLORS["text_white"], hover_color="#DC2626",
            command=self._on_delete
        )
        self.btn_delete.place(x=SIZES["city_card_w"] - 40, y=10)

        # Mini tiles container
        self.tiles_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tiles_frame.place(x=15, y=110, width=SIZES["city_card_w"] - 30, height=50)
        self.tiles_frame.bind("<Button-1>", self._on_click)

        self.l_feels = self._create_mini_tile(self.tiles_frame, "Feels Like", "--°", 0)
        self.l_hum = self._create_mini_tile(self.tiles_frame, "Humidity", "--%", 1)
        self.l_wind = self._create_mini_tile(self.tiles_frame, "Wind", "--", 2)

    def _create_mini_tile(self, parent, label_text, val_text, col):
        frame = ctk.CTkFrame(parent, fg_color=COLORS["city_card_sub"], corner_radius=8, height=45)
        frame.grid(row=0, column=col, padx=2, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_propagate(False)
        frame.bind("<Button-1>", self._on_click)
        
        lbl_title = ctk.CTkLabel(frame, text=label_text, font=("Segoe UI", 9), text_color="#A5B4FC")
        lbl_title.pack(pady=(2,0))
        lbl_title.bind("<Button-1>", self._on_click)
        
        lbl_val = ctk.CTkLabel(frame, text=val_text, font=("Segoe UI", 11, "bold"), text_color="white")
        lbl_val.pack()
        lbl_val.bind("<Button-1>", self._on_click)
        return lbl_val

    def _on_click(self, event):
        if self.on_click_callback:
            self.on_click_callback(self.city_name)

    def _on_delete(self):
        if self.on_delete_callback:
            self.on_delete_callback(self.city_id)

    def update_data(self, city_id, city_name, temp, condition, feels_like, humidity, wind):
        self.city_id = city_id
        self.city_name = city_name
        self.city_label.configure(text=city_name)
        self.temp_label.configure(text=f"{int(temp)}°")
        self.cond_label.configure(text=condition)
        
        self.l_feels.configure(text=f"{int(feels_like)}°")
        self.l_hum.configure(text=f"{int(humidity)}%")
        self.l_wind.configure(text=f"{int(wind)}")
