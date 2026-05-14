import os
import requests
from io import BytesIO
from PIL import Image
import customtkinter as ctk

class IconManager:
    _cache = {}

    @classmethod
    def get_icon(cls, icon_code, size=(50, 50)):
        cache_key = f"{icon_code}_{size[0]}x{size[1]}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        # Determine URL format based on desired size
        # We can use @4x for large icons
        if size[0] > 100:
            scale = "@4x"
        elif size[0] > 50:
            scale = "@2x"
        else:
            scale = ""

        url = f"https://openweathermap.org/img/wn/{icon_code}{scale}.png"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize(size, Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=size)
            cls._cache[cache_key] = ctk_img
            return ctk_img
        except Exception as e:
            print(f"Error loading icon {icon_code}: {e}")
            return None
