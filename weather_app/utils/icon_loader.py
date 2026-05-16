import os
from PIL import Image
import customtkinter as ctk

_cache = {}

def load_icon(filename, size=(24, 24), color="original"):
    """
    Loads an icon from the assets folder.
    filename: e.g. "sun.png"
    size: tuple, e.g. (24, 24)
    color: "original", "white", or "gray"
    """
    cache_key = f"{filename}_{size[0]}x{size[1]}_{color}"
    if cache_key in _cache:
        return _cache[cache_key]
        
    assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    path = os.path.join(assets_path, filename)
    
    if not os.path.exists(path):
        print(f"Icon not found: {filename}")
        # Return empty image of requested size to prevent crashes
        empty = Image.new("RGBA", size, (0, 0, 0, 0))
        img = ctk.CTkImage(light_image=empty, size=size)
        _cache[cache_key] = img
        return img
        
    try:
        pil_img = Image.open(path)
        if pil_img.mode != "RGBA":
            pil_img = pil_img.convert("RGBA")
            
        pil_img = pil_img.resize(size, Image.LANCZOS)
        
        if color != "original":
            # Mask coloring
            r_target, g_target, b_target = 255, 255, 255 # default white
            if color == "gray":
                # #9CA3AF is (156, 163, 175)
                r_target, g_target, b_target = 156, 163, 175
                
            colored_img = Image.new("RGBA", pil_img.size, (r_target, g_target, b_target, 255))
            colored_img.putalpha(pil_img.split()[3])
            pil_img = colored_img
            
        ctk_img = ctk.CTkImage(light_image=pil_img, size=size)
        _cache[cache_key] = ctk_img
        return ctk_img
        
    except Exception as e:
        print(f"Error processing icon {filename}: {e}")
        empty = Image.new("RGBA", size, (0, 0, 0, 0))
        return ctk.CTkImage(light_image=empty, size=size)

def get_weather_icon(icon_code, size=(50, 50), color="original"):
    mapping = {
        "01d": "sun.png", "01n": "sun.png",
        "02d": "cloud.png", "02n": "cloud.png",
        "03d": "cloud.png", "03n": "cloud.png",
        "04d": "cloud.png", "04n": "cloud.png",
        "09d": "rain.png", "09n": "rain.png",
        "10d": "rain.png", "10n": "rain.png",
        "11d": "rain.png", "11n": "rain.png", # Storm
        "13d": "cloud_white.png", "13n": "cloud_white.png", # Snow
        "50d": "cloud.png", "50n": "cloud.png", # Fog
    }
    filename = mapping.get(icon_code, "cloud.png")
    return load_icon(filename, size, color)
