import customtkinter as ctk
import tkinter as tk
from config import COLORS
from utils.icons import IconManager

class HourlyChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            width=900, 
            height=200, 
            fg_color="transparent",
            **kwargs
        )
        self.pack_propagate(False)

        self.canvas = tk.Canvas(
            self, 
            bg=COLORS["bg_card_light"], 
            highlightthickness=0
        )
        self.scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="bottom", fill="x", padx=20, pady=(0, 5))

    def _draw_gradient_pill(self, x, y0, y1, bar_width):
        r = bar_width / 2
        color_bottom = COLORS.get("chart_bar_tall", "#3B82F6")
        color_top = COLORS.get("chart_bar", "#93C5FD")
        
        def hex_to_rgb(hx):
            hx = hx.lstrip('#')
            return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
            
        r1, g1, b1 = hex_to_rgb(color_bottom)
        r2, g2, b2 = hex_to_rgb(color_top)
        
        h = y1 - y0
        if h > 0:
            for i in range(int(h)):
                ratio = i / h
                cr = int(r2 + (r1 - r2) * ratio)
                cg = int(g2 + (g1 - g2) * ratio)
                cb = int(b2 + (b1 - b2) * ratio)
                color = f"#{cr:02x}{cg:02x}{cb:02x}"
                # Extend 1px to avoid gaps
                self.canvas.create_rectangle(x - r, y0 + i, x + r, y0 + i + 1.5, fill=color, outline="")
                
        # Draw top cap only
        self.canvas.create_oval(x - r, y0 - r, x + r, y0 + r, outline="", fill=color_top)

    def update_data(self, hourly_data):
        self.canvas.delete("all")
        if not hourly_data:
            return

        width = 1680 
        height = 170
        max_h = 60
        
        self.canvas.configure(scrollregion=(0, 0, width, height))
        
        temps = [item.get('temp', 0) for item in hourly_data]
        min_t = min(temps)
        max_t = max(temps)
        diff = max_t - min_t if max_t != min_t else 1

        spacing = 70
        self.icon_images = []
        
        base_y = height - 60
        
        # Dashed line spanning the whole scrollable width
        self.canvas.create_line(10, base_y, width - 10, base_y, fill="#94A3B8", dash=(2, 4), width=1)

        for i, item in enumerate(hourly_data):
            t = item.get('temp', 0)
            norm = (t - min_t) / diff
            bar_h = 20 + (norm * (max_h - 20))
            
            x = 35 + i * spacing
            y1 = base_y # Flat bottom exactly on the line
            y0 = y1 - bar_h

            self._draw_gradient_pill(x, y0, y1, 28)
            
            # Draw Temp above bar
            self.canvas.create_text(
                x, y0 - 20, text=f"{int(t)}°", 
                fill=COLORS["text_secondary"], font=("Segoe UI", 12)
            )
            
            # Draw icon below line
            icon_code = item.get('icon_code', '01d')
            ctk_img = IconManager.get_icon(icon_code, size=(24, 24))
            if ctk_img:
                from PIL import ImageTk
                photo = ImageTk.PhotoImage(ctk_img.cget("light_image"))
                self.icon_images.append(photo)
                self.canvas.create_image(x, base_y + 20, image=photo)
            
            # Draw time below icon
            dt_str = item.get('datetime', '')
            time_str = dt_str.split(' ')[1][:5] if ' ' in dt_str else ""
            self.canvas.create_text(
                x, base_y + 45, text=time_str, 
                fill=COLORS["text_secondary"], font=("Segoe UI", 10)
            )
