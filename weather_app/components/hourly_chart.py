import customtkinter as ctk
from config import COLORS
from utils.icons import IconManager

class HourlyChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=180, fg_color="transparent", **kwargs)
        self.pack_propagate(False)

        self.canvas = ctk.CTkCanvas(
            self, bg=COLORS["bg_card"], highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

    def update_data(self, hourly_data):
        self.canvas.delete("all")
        if not hourly_data:
            return

        width = 860 # self.winfo_width() is unreliable during init, fixed to inner card width roughly
        height = 180
        max_h = 100
        
        temps = [item.get('temp', 0) for item in hourly_data]
        min_t = min(temps)
        max_t = max(temps)
        diff = max_t - min_t if max_t != min_t else 1

        # We need to fit 8 or more items evenly
        num_items = len(hourly_data)
        spacing = width / (num_items + 1)
        
        self.icon_images = [] # Prevent garbage collection
        
        for i, item in enumerate(hourly_data):
            t = item.get('temp', 0)
            norm = (t - min_t) / diff
            bar_h = 20 + (norm * (max_h - 20))
            
            x = spacing + i * spacing
            y1 = height - 50 
            y0 = y1 - bar_h

            # Use create_line with round caps for the thick bars
            self.canvas.create_line(x, y0, x, y1, fill=COLORS["chart_bar"], width=30, capstyle="round")
            
            # Draw Temp above bar
            self.canvas.create_text(
                x, y0 - 15, text=f"{int(t)}°", 
                fill=COLORS["text_secondary"], font=("Segoe UI", 10)
            )
            
            # Draw icon below bar
            icon_code = item.get('icon_code', '01d')
            ctk_img = IconManager.get_icon(icon_code, size=(40, 40))
            if ctk_img:
                photo_img = ctk_img.cget("light_image")
                # Need to convert PIL Image to PhotoImage since cget returns PIL Image
                from PIL import ImageTk
                photo = ImageTk.PhotoImage(photo_img)
                self.icon_images.append(photo)
                self.canvas.create_image(x, y1 + 15, image=photo)
            else:
                self.canvas.create_text(
                    x, y1 + 15, text="☁️", 
                    fill=COLORS["text_primary"], font=("Segoe UI", 14)
                )
            
            # Draw time below icon
            dt_str = item.get('datetime', '')
            time_str = dt_str.split(' ')[1][:5] if ' ' in dt_str else ""
            self.canvas.create_text(
                x, y1 + 35, text=time_str, 
                fill=COLORS["text_secondary"], font=("Segoe UI", 9)
            )

        # Draw a custom scrollbar-like indicator at the very bottom
        sb_width = 100
        self.canvas.create_line(width/2 - sb_width/2, height - 10, width/2 + sb_width/2, height - 10, fill="#CBD5E1", width=4, capstyle="round")
