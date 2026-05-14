"""
Configuration constants for the Weather Forecast Application.
"""

OWM_API_KEY = "f0070f4e338513f27ceb7f7f67f1bb47"  # Placeholder as requested by the user

COLORS = {
    # Page background
    "bg_page":         "#E8EEF7",   # Light blueish background
    "bg_card":         "#FFFFFF",   # White cards
    "bg_main_card":    "#6B7B94",   # Dark grey main card (city + weather)

    # Accent colors - "Weather Forecast" title
    "accent_blue":     "#4A7AE8",   # "Weather" (blue)
    "accent_purple":   "#8B5CF6",   # "Forecast" (purple)

    # Menu (sidebar)
    "menu_header_bg":  "#7C3AED",   # Gradient from blue to purple (top)
    "menu_header_bg2": "#3B82F6",   # (bottom of gradient)
    "menu_item_bg":    "#F3F4F6",   # Menu item background
    "menu_item_hover": "#E5E7EB",

    # Stat tiles (icons)
    "icon_humidity":   "#3B82F6",   # Blue (Humidity)
    "icon_wind":       "#10B981",   # Green (Wind Speed)
    "icon_visibility": "#8B5CF6",   # Purple (Visibility)
    "icon_pressure":   "#F97316",   # Orange (Pressure)
    "icon_dew":        "#EC4899",   # Pink (Dew Point)
    "icon_uv":         "#EAB308",   # Yellow (UV Index)

    # Temperature chart
    "chart_bar":       "#93C5FD",   # Light blue bar
    "chart_bar_tall":  "#3B82F6",   # Dark blue for tall bars

    # 7-Day Forecast - temperature bar
    "temp_bar_cold":   "#86EFAC",   # Green (min temp)
    "temp_bar_hot":    "#FDE047",   # Yellow (max temp)

    # Saved cities cards
    "city_card_bg":    "#3730A3",   # Dark blue/purple
    "city_card_sub":   "#4F46E5",   # Shade for tiles inside the card

    # "Search" button
    "btn_search_bg":   "#111827",   # Almost black
    "btn_search_text": "#FFFFFF",

    # Text
    "text_primary":    "#111827",
    "text_secondary":  "#6B7280",
    "text_white":      "#FFFFFF",
    "text_link":       "#3B82F6",   # Popular cities links
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
