"""
Configuration constants for the Weather Forecast Application.
"""

OWM_API_KEY = "f0070f4e338513f27ceb7f7f67f1bb47"  # Placeholder as requested by the user

COLORS = {
    # Page background
    "bg_page":         "#F3F7FF",   # Soft light blue background
    "bg_gradient_top": "#E8F0FF",   # Gradient start for large background areas
    "bg_gradient_bottom": "#F8FBFF",   # Gradient end for large background areas
    "bg_card":         "#FFFFFF",   # White cards
    "bg_card_light":   "#F8FAFF",   # Slight off-white cards for separation
    "bg_main_card":    "#556A96",   # Dark blue main card
    "bg_main_card_alt":"#42618C",   # Alternative darker shade for main card

    # Accent colors
    "accent_blue":     "#4A7AE8",   # "Weather" (blue)
    "accent_purple":   "#8B5CF6",   # "Forecast" (purple)
    "accent_gradient": ("#7C3AED", "#3B82F6"), # Purple to Blue gradient

    # Menu (sidebar)
    "menu_header_bg":  "#7C3AED",
    "menu_header_bg2": "#3B82F6",
    "menu_item_bg":    "#F3F4F6",
    "menu_item_hover": "#E5E7EB",
    "menu_icon_saved": "#0EA5E9",   # Light blue for Saved Cities icon box
    "menu_icon_set":   "#D946EF",   # Pink/Purple for Settings icon box

    # Stat tiles (icons)
    "icon_humidity":   "#3B82F6",
    "icon_wind":       "#10B981",
    "icon_visibility": "#8B5CF6",
    "icon_pressure":   "#F97316",
    "icon_dew":        "#EC4899",
    "icon_uv":         "#EAB308",

    # Text
    "text_primary":    "#111827",
    "text_secondary":  "#6B7280",
    "text_white":      "#FFFFFF",
    "text_link":       "#3B82F6",
    "btn_search_bg":   "#4A7AE8",   # Matching accent_blue
    "chart_bar":       "#4A7AE8",   # Main blue color for bars
    "temp_bar_hot":    "#F97316",   # Orange for warmer days
    "temp_bar_cold":   "#3B82F6",   # Blue for colder days
}

# Icon Mapping (Asset filenames)
ICONS = {
    "location":   "location.png",
    "settings":   "settings.png",
    "humidity":   "humidity.png",
    "wind":       "wind.png",
    "visibility": "visibility.png",
    "pressure":   "pressure.png",
    "dew_point":  "dew_point.png",
    "uv_index":   "uv_index.png",
    "trash":      "trash.png",
    "globe":      "globe.png",
    "sun":        "sun.png",
    "cloud":      "cloud.png",
    "cloud_white":"cloud_white.png",
    "rain":       "rain.png",
}

FONTS = {
    "title_large":  ("Segoe UI", 32, "bold"),     # "Weather Forecast"
    "subtitle":     ("Segoe UI", 12, "normal"),   # Subtitle
    "temp_big":     ("Segoe UI", 42, "bold"),     # Big temperature
    "temp_unit":    ("Segoe UI", 22, "normal"),   # "°C"
    "city_name":    ("Segoe UI", 20, "bold"),     # City name
    "date_text":    ("Segoe UI", 11, "normal"),   # Date
    "condition":    ("Segoe UI", 16, "normal"),   # "Partly Cloudy"
    "feels_like":   ("Segoe UI", 11, "normal"),   # "Feels like 16°C"
    "stat_label":   ("Segoe UI", 11, "normal"),   # "Humidity"
    "stat_value":   ("Segoe UI", 14, "bold"),     # "65%"
    "chart_temp":   ("Segoe UI", 10, "normal"),   # Temp on chart
    "week_day":     ("Segoe UI", 13, "normal"),   # "Monday"
    "week_cond":    ("Segoe UI", 13, "normal"),   # "Sunny"
    "section_head": ("Segoe UI", 16, "bold"),     # "Today's Temperature"
    "search_input": ("Segoe UI", 13, "normal"),   # Search field
    "btn_text":     ("Segoe UI", 13, "bold"),     # Buttons
    "menu_title":   ("Segoe UI", 22, "bold"),     # "Menu"
    "menu_sub":     ("Segoe UI", 12, "normal"),   # Menu subtitle
}

SIZES = {
    "window_default":   (1100, 850),  # Default window size
    "window_min":       (900, 700),   # Min size

    # Stat tiles
    "stat_tile_w":      130,
    "stat_tile_h":      90,
    "stat_icon_box":    36,           # Fixed square for icon
    "stat_icon_size":   20,           # Icon size inside

    # Main card
    "main_card_h":      190,
    "weather_icon_size": 80,          # Fixed icon size

    # Chart
    "chart_bar_w":      28,           # Fixed bar width
    "chart_max_h":      80,           # Max bar height

    # Saved city card
    "city_card_w":      300,
    "city_card_h":      180,

    # Sidebar menu
    "menu_panel_w":     280,

    # Weather icons in 7-day forecast
    "forecast_icon":    28,           # FIXED
}
