import os
from PIL import Image
import customtkinter as ctk

class IconManager:
    _cache = {}
    _assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

    @classmethod
    def get_icon(cls, icon_code, size=(50, 50)):
        cache_key = f"{icon_code}_{size[0]}x{size[1]}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        # Mapping OpenWeatherMap codes to local assets
        mapping = {
            "01d": "sun.png",
            "01n": "sun.png",
            "02d": "cloud.png",
            "02n": "cloud.png",
            "03d": "cloud.png",
            "03n": "cloud.png",
            "04d": "cloud.png",
            "04n": "cloud.png",
            "09d": "rain.png",
            "09n": "rain.png",
            "10d": "rain.png",
            "10n": "rain.png",
            "11d": "rain.png", # Storm
            "11n": "rain.png",
            "13d": "cloud_white.png", # Snow
            "13n": "cloud_white.png",
            "50d": "cloud.png", # Fog
            "50n": "cloud.png",
        }

        filename = mapping.get(icon_code, "cloud.png")
        if size[0] >= 100 and "cloud" in filename:
            filename = "cloud_main.png"
            
        path = os.path.join(cls._assets_path, filename)
        
        try:
            if os.path.exists(path):
                img_data = Image.open(path)
                # For white cloud on dark background, we might want to check the context
                # but for now let's just use what's mapped
                img_data = img_data.resize(size, Image.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img_data, size=size)
                cls._cache[cache_key] = ctk_img
                return ctk_img
            return None
        except Exception as e:
            print(f"Error loading local icon {icon_code}: {e}")
            return None

    @classmethod
    def get_local_icon(cls, filename, size=(24, 24)):
        cache_key = f"local_{filename}_{size[0]}x{size[1]}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        path = os.path.join(cls._assets_path, filename)
        if os.path.exists(path):
            img = Image.open(path).resize(size, Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, size=size)
            cls._cache[cache_key] = ctk_img
            return ctk_img
        return None
