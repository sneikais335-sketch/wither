import customtkinter as ctk
from PIL import Image, ImageDraw
import urllib.request
import urllib.parse
import json
import datetime
import os
import xml.etree.ElementTree as ET
import subprocess
import io
import re

# ==========================================
# Вставьте сюда ваш API-ключ от OpenWeatherMap (если есть)
# ==========================================
OPENWEATHER_API_KEY = ""

# Appearance and Font settings
ctk.set_appearance_mode("Light")
MAIN_FONT = "Inter"

# Custom inline SVG definitions
CALENDAR_SVG = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="4" width="18" height="17" rx="3" stroke="#14142B" stroke-width="2" stroke-linejoin="round"/>
  <line x1="3" y1="9" x2="21" y2="9" stroke="#14142B" stroke-width="2"/>
  <line x1="8" y1="2" x2="8" y2="5" stroke="#14142B" stroke-width="2" stroke-linecap="round"/>
  <line x1="16" y1="2" x2="16" y2="5" stroke="#14142B" stroke-width="2" stroke-linecap="round"/>
  <circle cx="8" cy="13" r="1.2" fill="#14142B"/>
  <circle cx="12" cy="13" r="1.2" fill="#14142B"/>
  <circle cx="16" cy="13" r="1.2" fill="#14142B"/>
  <circle cx="8" cy="17" r="1.2" fill="#14142B"/>
  <circle cx="12" cy="17" r="1.2" fill="#14142B"/>
  <circle cx="16" cy="17" r="1.2" fill="#14142B"/>
</svg>"""

HAMBURGER_SVG = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 6H20M4 12H20M4 18H20" stroke="#14142B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

SEARCH_SVG = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="11" cy="11" r="7" stroke="#6E7191" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M20 20L16 16" stroke="#6E7191" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

TRANSLATIONS = {
    "EN": {
        "app_title": "Weather Forecast",
        "app_subtitle": "Your personal weather companion for accurate forecasts worldwide",
        "menu_title": "Menu",
        "menu_subtitle": "Manage your weather preferences",
        "saved_cities": "Saved Cities",
        "settings": "Settings",
        "language": "Language",
        "search_placeholder": "Search for a city or location...",
        "search_btn": "Search",
        "save_btn": "♡ Save",
        "saved_btn": "♥ Saved",
        "popular": "📍 Popular: San Francisco  New York  London  Tokyo  Paris",
        "feels_like": "Feels like",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "visibility": "Visibility",
        "pressure": "Pressure",
        "dew_point": "Dew Point",
        "uv_index": "UV Index",
        "todays_temp": "Today's Temperature",
        "7day_forecast": "7-Day Forecast",
        "home_btn": "← Home",
        "saved_title": "Saved Cities",
        "saved_sub": "Your favorite locations at a glance",
        "export_btn": "⬇ Export All to Excel",
        "settings_title": "Settings",
        "settings_sub": "Customize your weather experience",
        "display": "Display",
        "temp_unit": "Temperature Unit",
        "temp_unit_desc": "Choose between Celsius and Fahrenheit",
        "dark_mode": "Dark Mode",
        "dark_mode_desc": "Toggle dark theme (Coming Soon)",
        "notifications": "Notifications",
        "weather_alerts": "Weather Alerts",
        "weather_alerts_desc": "Get notified about severe weather",
        "location": "Location",
        "auto_detect": "Auto-detect Location",
        "auto_detect_desc": "Automatically detect your current location"
    },
    "RU": {
        "app_title": "Прогноз погоды",
        "app_subtitle": "Ваш личный помощник для точных прогнозов",
        "menu_title": "Меню",
        "menu_subtitle": "Настройки приложения",
        "saved_cities": "Сохраненные",
        "settings": "Настройки",
        "language": "Язык",
        "search_placeholder": "Поиск города...",
        "search_btn": "Найти",
        "save_btn": "♡ Сохранить",
        "saved_btn": "♥ Сохранено",
        "popular": "📍 Популярные: Москва  Нью-Йорк  Лондон  Токио  Париж",
        "feels_like": "Ощущается как",
        "humidity": "Влажность",
        "wind_speed": "Ветер",
        "visibility": "Видимость",
        "pressure": "Давление",
        "dew_point": "Точка росы",
        "uv_index": "УФ-индекс",
        "todays_temp": "Сегодня",
        "7day_forecast": "Прогноз на 7 дней",
        "home_btn": "← Главная",
        "saved_title": "Сохраненные",
        "saved_sub": "Любимые локации",
        "export_btn": "⬇ Экспорт в Excel",
        "settings_title": "Настройки",
        "settings_sub": "Управление приложением",
        "display": "Внешний вид",
        "temp_unit": "Единицы измерения",
        "temp_unit_desc": "Цельсий или Фаренгейт",
        "dark_mode": "Темная тема",
        "dark_mode_desc": "Включить (скоро)",
        "notifications": "Уведомления",
        "weather_alerts": "Штормовые предупреждения",
        "weather_alerts_desc": "Получать важные оповещения",
        "location": "Геопозиция",
        "auto_detect": "Авто-определение",
        "auto_detect_desc": "Использовать GPS"
    },
    "KG": {
        "app_title": "Аба ырайы",
        "app_subtitle": "Сиздин жеке жардамчыңыз",
        "menu_title": "Меню",
        "menu_subtitle": "Жөндөөлөрдү башкаруу",
        "saved_cities": "Сакталгандар",
        "settings": "Жөндөөлөр",
        "language": "Тил",
        "search_placeholder": "Шаарды издөө...",
        "search_btn": "Издөө",
        "save_btn": "♡ Сактоо",
        "saved_btn": "♥ Сакталды",
        "popular": "📍 Белгилүүлөр: Бишкек  Ош  Москва  Нью-Йорк",
        "feels_like": "Сезгилет",
        "humidity": "Нымдуулук",
        "wind_speed": "Шамал",
        "visibility": "Көрүнүмдүүлүк",
        "pressure": "Басым",
        "dew_point": "Шүүдүрүм чекити",
        "uv_index": "УФ-индекси",
        "todays_temp": "Бүгүн",
        "7day_forecast": "7 күндүк прогноз",
        "home_btn": "← Башкы",
        "saved_title": "Сакталган шаарлар",
        "saved_sub": "Сүйүктүү жерлериңиз",
        "export_btn": "⬇ Excel'ге жүктөө",
        "settings_title": "Жөндөөлөр",
        "settings_sub": "Өзүңүзге ылайыктаңыз",
        "display": "Дисплей",
        "temp_unit": "Температура",
        "temp_unit_desc": "Цельсий же Фаренгейт",
        "dark_mode": "Караңгы тема",
        "dark_mode_desc": "Күйгүзүү (жакында)",
        "notifications": "Билдирмелер",
        "weather_alerts": "Эскертүүлөр",
        "weather_alerts_desc": "Кескин өзгөрүүлөр жөнүндө билдирүү",
        "location": "Жайгашкан жер",
        "auto_detect": "Авто-аныктоо",
        "auto_detect_desc": "GPS колдонуу"
    }
}


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weather Forecast Pro")
        self.geometry("1100x900")
        self.configure(fg_color="#F3F6FB")

        self.menu_visible = False
        self.menu_animating = False
        self._menu_x = -500
        self.calendar_visible = False
        self.current_lang = "EN"
        self.temp_unit = "C"
        self.font_family = MAIN_FONT
        self.current_screen = "main"

        self.dynamic_labels = []
        self.saved_cities = []
        self.current_city = "Bishkek"

        now = datetime.datetime.now()
        self.current_cal_year = now.year
        self.current_cal_month = now.month

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew")

        self.sidebar_calendar = ctk.CTkFrame(self, fg_color="#FFFFFF", width=300, corner_radius=20,
                                             border_width=1, border_color="#E2E8F0")
        self.create_calendar_widget()

        self.menu_frame = ctk.CTkFrame(self, width=280, height=380, fg_color="#FFFFFF", corner_radius=20,
                                       border_width=1, border_color="#E2E8F0")
        self.menu_frame.place(x=self._menu_x, y=80)

        self.build_menu()
        self.svg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Untitled(6) (2)")

        self.bind("<Configure>", self.on_resize)
        self.show_main_screen()
        self.apply_language()

    def on_resize(self, event):
        if event.widget == self:
            width = event.width
            if width > 1050:
                pad = (width - 1050) // 2
                self.main_container.grid_configure(padx=(pad, pad))
            else:
                self.main_container.grid_configure(padx=0)

    # ==========================================
    # SVG UTILS
    # ==========================================
    def load_svg_image(self, file_name, size, color=None):
        if not file_name: return None
        file_path = os.path.join(self.svg_dir, file_name)
        if not os.path.exists(file_path): return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                svg_text = f.read()
            return self.load_svg_from_string(svg_text, size, color)
        except:
            return None

    def load_svg_from_string(self, svg_text, size, color=None):
        try:
            ET.register_namespace('', 'http://www.w3.org/2000/svg')
            root = ET.fromstring(svg_text)
            root.attrib['width'] = str(size[0])
            root.attrib['height'] = str(size[1])
            if color:
                for el in root.iter():
                    if 'stroke' in el.attrib and el.attrib['stroke'] != 'none':
                        el.attrib['stroke'] = color
                    if 'fill' in el.attrib and el.attrib['fill'] != 'none' and not el.attrib['fill'].startswith('url('):
                        el.attrib['fill'] = color
            svg_bytes = ET.tostring(root, encoding='utf-8')
            p = subprocess.run(['convert', '-background', 'none', 'svg:-', 'png:-'], input=svg_bytes,
                               capture_output=True)
            if p.returncode == 0 and p.stdout:
                img = Image.open(io.BytesIO(p.stdout))
                return ctk.CTkImage(light_image=img, size=size)
            return None
        except:
            return None

    # ==========================================
    # DATE LOCALIZATION HELPER
    # ==========================================
    def get_localized_date_long(self, dt):
        wd_idx = dt.weekday()
        m_idx = dt.month - 1

        wd_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        wd_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        wd_kg = ["Дүйшөмбү", "Шейшемби", "Шаршемби", "Бейшемби", "Жума", "Ишемби", "Жекшемби"]

        m_en = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"]
        m_ru = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                "Ноября", "Декабря"]
        m_kg = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
                "Декабрь"]

        if self.current_lang == "RU":
            return f"{wd_ru[wd_idx]}, {dt.day} {m_ru[m_idx]} {dt.year}"
        elif self.current_lang == "KG":
            return f"{wd_kg[wd_idx]}, {dt.day} {m_kg[m_idx]} {dt.year}"
        else:
            return f"{wd_en[wd_idx]}, {m_en[m_idx]} {dt.day}, {dt.year}"

    # ==========================================
    # I18N UTILS
    # ==========================================
    def get_text(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def register_i18n(self, widget, key, attr="text"):
        self.dynamic_labels.append({"widget": widget, "key": key, "attr": attr})
        return self.get_text(key)

    def apply_language(self):
        for item in self.dynamic_labels:
            try:
                if item["attr"] == "text":
                    item["widget"].configure(text=self.get_text(item["key"]))
                elif item["attr"] == "placeholder_text":
                    item["widget"].configure(placeholder_text=self.get_text(item["key"]))
            except:
                pass
        self.update_lang_buttons()
        if hasattr(self, 'update_popular_cities'):
            self.update_popular_cities()

    def update_popular_cities(self):
        if not hasattr(self, 'pop_frame') or not self.pop_frame.winfo_exists(): return
        for child in self.pop_frame.winfo_children(): child.destroy()
        text = self.get_text("popular")
        parts = text.split(":", 1)
        prefix = parts[0].strip() + ":" if len(parts) == 2 else ""
        cities_str = parts[1] if len(parts) == 2 else text
        if prefix:
            ctk.CTkLabel(self.pop_frame, text=prefix, font=(self.font_family, 11), text_color="#6E7191").pack(
                side="left", padx=(0, 5))
        cities = [c.strip() for c in cities_str.split("  ") if c.strip()]
        for city in cities:
            btn = ctk.CTkButton(self.pop_frame, text=city, font=(self.font_family, 11, "underline"),
                                fg_color="transparent",
                                text_color="#3B82F6", hover_color="#E8EEF4", height=20, width=0,
                                cursor="hand2", command=lambda c=city: self.fetch_weather(c))
            btn.pack(side="left", padx=2)

    # ==========================================
    # UTILITIES
    # ==========================================
    def create_gradient_image(self, width, height, color1, color2, vertical=False):
        image = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(image)
        hex_to_rgb = lambda h: tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)
        if vertical:
            for y in range(height):
                ratio = y / height
                draw.line([(0, y), (width, y)],
                          fill=(int(r1 + (r2 - r1) * ratio), int(g1 + (g2 - g1) * ratio), int(b1 + (b2 - b1) * ratio),
                                255))
        else:
            for x in range(width):
                ratio = x / width
                draw.line([(x, 0), (x, height)],
                          fill=(int(r1 + (r2 - r1) * ratio), int(g1 + (g2 - g1) * ratio), int(b1 + (b2 - b1) * ratio),
                                255))
        return ctk.CTkImage(light_image=image, size=(width, height))

    def get_gradient_bar_image(self, width, height, color1, color2):
        image = Image.new("RGBA", (width * 2, height * 2), (255, 255, 255, 0))
        hex_to_rgb = lambda h: tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)
        grad = Image.new("RGBA", (width * 2, height * 2))
        grad_draw = ImageDraw.Draw(grad)
        for y in range(height * 2):
            ratio = y / (height * 2)
            grad_draw.line([(0, y), (width * 2, y)],
                           fill=(int(r1 + (r2 - r1) * ratio), int(g1 + (g2 - g1) * ratio), int(b1 + (b2 - b1) * ratio),
                                 255))
        mask = Image.new("L", (width * 2, height * 2), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, width * 2, height * 2], radius=width, fill=255)
        grad.putalpha(mask)
        grad = grad.resize((width, height), Image.LANCZOS)
        return ctk.CTkImage(light_image=grad, size=(width, height))

    def create_rounded_gradient_bar(self, parent, width, height, color1, color2):
        img = self.get_gradient_bar_image(width, height, color1, color2)
        return ctk.CTkLabel(parent, text="", image=img)

    def clear_screen(self):
        for widget in self.main_container.winfo_children(): widget.destroy()
        self.dynamic_labels = [item for item in self.dynamic_labels if item["widget"].winfo_exists()]

    # ==========================================
    # MENU & ANIMATION LOGIC
    # ==========================================
    def create_menu_btn(self, parent, icon_char, icon_color, text_key, command):
        btn_frame = ctk.CTkFrame(parent, fg_color="#F8F9FA", corner_radius=15, height=60)
        btn_frame.pack(fill="x", padx=15, pady=8)
        btn_frame.pack_propagate(False)
        btn = ctk.CTkButton(btn_frame, text="", fg_color="transparent", hover_color="rgba(0,0,0,0.05)",
                            corner_radius=15, command=command)
        btn.place(relx=0, rely=0, relwidth=1, relheight=1)
        icon_lbl = ctk.CTkLabel(btn_frame, text=icon_char, font=(self.font_family, 18), text_color="#FFFFFF",
                                fg_color=icon_color, width=36, height=36, corner_radius=10)
        icon_lbl.place(x=15, rely=0.5, anchor="w")
        text_lbl = ctk.CTkLabel(btn_frame, font=(self.font_family, 14, "bold"), text_color="#14142B")
        text_lbl.place(x=65, rely=0.5, anchor="w")
        self.register_i18n(text_lbl, text_key)
        icon_lbl.bind("<Button-1>", lambda e: command())
        text_lbl.bind("<Button-1>", lambda e: command())

    def build_menu(self):
        header_frame = ctk.CTkFrame(self.menu_frame, fg_color="#6D3BFE", corner_radius=16)
        header_frame.pack(fill="x", padx=10, pady=10)
        menu_title = ctk.CTkLabel(header_frame, font=(self.font_family, 22, "bold"), text_color="#FFFFFF")
        menu_title.pack(anchor="w", padx=20, pady=(20, 0))
        self.register_i18n(menu_title, "menu_title")
        menu_sub = ctk.CTkLabel(header_frame, font=(self.font_family, 11), text_color="#E2E8F0")
        menu_sub.pack(anchor="w", padx=20, pady=(5, 20))
        self.register_i18n(menu_sub, "menu_subtitle")
        self.create_menu_btn(self.menu_frame, "📍", "#25A0E8", "saved_cities", self.show_saved_cities_screen)
        self.create_menu_btn(self.menu_frame, "⚙", "#DE3196", "settings", self.show_settings_screen)
        lang_lbl = ctk.CTkLabel(self.menu_frame, font=(self.font_family, 13, "bold"), text_color="#6E7191")
        lang_lbl.pack(anchor="w", padx=20, pady=(20, 5))
        self.register_i18n(lang_lbl, "language")
        lang_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        lang_frame.pack(fill="x", padx=15, pady=5)
        self.lang_buttons = {}
        for lang in ["EN", "RU", "KG"]:
            btn = ctk.CTkButton(lang_frame, text=lang, font=(self.font_family, 13, "bold"), height=55, corner_radius=12,
                                command=lambda l=lang: self.set_language(l))
            btn.pack(side="left", padx=4, expand=True, fill="x")
            self.lang_buttons[lang] = btn

    def set_language(self, lang):
        self.current_lang = lang
        self.apply_language()
        if getattr(self, 'current_screen', 'main') == "main":
            self.show_main_screen()
        elif self.current_screen == "saved":
            self.show_saved_cities_screen()
        elif self.current_screen == "settings":
            self.show_settings_screen()

    def update_lang_buttons(self):
        for lang, btn in self.lang_buttons.items():
            if lang == self.current_lang:
                btn.configure(fg_color="#6D3BFE", text_color="#FFFFFF", hover_color="#563BFE", text=f"{lang}\n✓")
            else:
                btn.configure(fg_color="#F8F9FA", text_color="#14142B", hover_color="#E2E8F0", text=lang)

    def toggle_menu(self):
        if self.menu_animating: return
        self.menu_animating = True
        if self.menu_visible:
            self.animate_menu(-500)
        else:
            self.menu_frame.lift();
            self.animate_menu(30)

    def animate_menu(self, target_x):
        step = (target_x - self._menu_x) * 0.2
        if abs(target_x - self._menu_x) < 2:
            self._menu_x = target_x
            self.menu_frame.place(x=target_x)
            self.menu_visible = target_x > 0
            self.menu_animating = False
        else:
            self._menu_x += step
            self.menu_frame.place(x=int(self._menu_x))
            self.after(16, lambda: self.animate_menu(target_x))

    # ==========================================
    # CALENDAR WIDGET
    # ==========================================
    def create_calendar_widget(self):
        now = datetime.datetime.now()
        cal_box = ctk.CTkFrame(self.sidebar_calendar, fg_color="transparent")
        cal_box.pack(fill="x", padx=20, pady=20)
        header_row = ctk.CTkFrame(cal_box, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 20))
        ctk.CTkButton(header_row, text="<", font=(self.font_family, 14), width=25, height=25, fg_color="transparent",
                      text_color="#A0AEC0", hover_color="#F0F0F0").pack(side="left")
        ctk.CTkLabel(header_row, text=now.strftime("%B %Y"), font=(self.font_family, 14, "bold"),
                     text_color="#4B5563").pack(side="left", expand=True)
        ctk.CTkButton(header_row, text=">", font=(self.font_family, 14), width=25, height=25, fg_color="transparent",
                      text_color="#A0AEC0", hover_color="#F0F0F0").pack(side="right")
        days_grid = ctk.CTkFrame(cal_box, fg_color="transparent")
        days_grid.pack(fill="x")
        for col in range(7): days_grid.grid_columnconfigure(col, weight=1)
        headers = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for idx, h in enumerate(headers):
            ctk.CTkLabel(days_grid, text=h, font=(self.font_family, 10, "bold"), text_color="#D1D5DB").grid(row=0,
                                                                                                            column=idx,
                                                                                                            pady=(0,
                                                                                                                  15))
        day_counter = 1
        self.day_buttons = []
        for r in range(1, 6):
            for c in range(7):
                if day_counter <= 31:
                    btn = ctk.CTkButton(days_grid, text=str(day_counter), font=(self.font_family, 12, "normal"),
                                        text_color="#4B5563", fg_color="transparent", hover_color="#E5E7EB",
                                        corner_radius=15, width=30, height=30, border_width=0)
                    btn.grid(row=r, column=c, pady=5, padx=2)
                    btn.configure(command=lambda b=btn, d=day_counter: self.select_date(b, d))
                    self.day_buttons.append({"widget": btn, "day": day_counter})
                    day_counter += 1

    def select_date(self, selected_btn, day):
        for item in self.day_buttons:
            btn = item["widget"]
            if btn == selected_btn:
                btn.configure(fg_color="#10B981", text_color="#FFFFFF", font=(self.font_family, 12, "bold"),
                              hover_color="#059669")
            else:
                btn.configure(fg_color="transparent", text_color="#4B5563", font=(self.font_family, 12, "normal"),
                              hover_color="#E5E7EB")
        selected_date = datetime.datetime(self.current_cal_year, self.current_cal_month, day)
        if hasattr(self, 'date_lbl') and self.date_lbl.winfo_exists():
            self.date_lbl.configure(text=selected_date.strftime("%d.%m.%Y"))
        if hasattr(self, 'main_date_lbl') and self.main_date_lbl.winfo_exists():
            self.main_date_lbl.configure(text=self.get_localized_date_long(selected_date))
        self.fetch_weather(self.current_city, target_date=selected_date)

    def toggle_calendar(self):
        if self.calendar_visible:
            self.sidebar_calendar.place_forget()
            self.calendar_visible = False
        else:
            self.sidebar_calendar.lift()
            self.sidebar_calendar.place(in_=self.main_container, relx=1.0, y=95, x=-10, anchor="ne")
            self.calendar_visible = True

    # ==========================================
    # COMMON COMPONENTS
    # ==========================================
    def build_header(self, parent, is_main=False, title_text=""):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10), padx=30)
        if is_main:
            burg_img = self.load_svg_from_string(HAMBURGER_SVG, (20, 20), "#14142B")
            burger_btn = ctk.CTkButton(header_frame, text="" if burg_img else "☰", image=burg_img, width=45, height=45,
                                       fg_color="#FFFFFF", text_color="#14142B", corner_radius=12,
                                       hover_color="#F0F0F0", command=self.toggle_menu)
            burger_btn.pack(side="left", anchor="n")
            date_container = ctk.CTkFrame(header_frame, fg_color="#E8EEF4", border_width=0, corner_radius=16)
            date_container.pack(side="right", anchor="n")
            cal_img = self.load_svg_from_string(CALENDAR_SVG, (22, 22), "#14142B")
            icon_lbl = ctk.CTkLabel(date_container, text="" if cal_img else "🗓", image=cal_img,
                                    font=(self.font_family, 26), text_color="#14142B")
            icon_lbl.pack(side="left", padx=(15, 10), pady=6)
            text_frame = ctk.CTkFrame(date_container, fg_color="transparent")
            text_frame.pack(side="left", padx=(0, 15), pady=6)
            self.header_city_lbl = ctk.CTkLabel(text_frame, text=self.current_city, font=(self.font_family, 13),
                                                text_color="#6E7191")
            self.header_city_lbl.pack(anchor="w", pady=0)
            date_str = datetime.datetime.now().strftime("%d.%m.%Y")
            self.date_lbl = ctk.CTkLabel(text_frame, text=date_str, font=(self.font_family, 16, "bold"),
                                         text_color="#14142B")
            self.date_lbl.pack(anchor="w", pady=0)
            date_container.bind("<Button-1>", lambda e: self.toggle_calendar())
            icon_lbl.bind("<Button-1>", lambda e: self.toggle_calendar())
            text_frame.bind("<Button-1>", lambda e: self.toggle_calendar())
            self.header_city_lbl.bind("<Button-1>", lambda e: self.toggle_calendar())
            self.date_lbl.bind("<Button-1>", lambda e: self.toggle_calendar())
            center_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            center_frame.pack(expand=True)
            title_lbl = ctk.CTkLabel(center_frame, font=(self.font_family, 36, "bold"), text_color="#7E3BFE")
            title_lbl.pack()
            self.register_i18n(title_lbl, "app_title")
            sub_lbl = ctk.CTkLabel(center_frame, font=(self.font_family, 12), text_color="#6E7191")
            sub_lbl.pack()
            self.register_i18n(sub_lbl, "app_subtitle")
        else:
            home_btn = ctk.CTkButton(header_frame, font=(self.font_family, 13, "bold"), width=80, height=40,
                                     fg_color="#FFFFFF", text_color="#6D3BFE", corner_radius=10, hover_color="#F0F0F0",
                                     command=self.show_main_screen)
            home_btn.place(relx=0, rely=0)
            self.register_i18n(home_btn, "home_btn")
            center_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            center_frame.pack(expand=True)
            title_lbl = ctk.CTkLabel(center_frame, font=(self.font_family, 36, "bold"), text_color="#7E3BFE")
            title_lbl.pack()
            self.register_i18n(title_lbl, title_text)
            sub_text = "saved_sub" if title_text == "saved_title" else "settings_sub"
            sub_lbl = ctk.CTkLabel(center_frame, font=(self.font_family, 12), text_color="#6E7191")
            sub_lbl.pack()
            self.register_i18n(sub_lbl, sub_text)

    # ==========================================
    # SCREEN 1: MAIN WEATHER
    # ==========================================
    def show_main_screen(self):
        self.current_screen = "main"
        self.clear_screen()
        if self.menu_visible: self.toggle_menu()
        scroll_canvas = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll_canvas.pack(fill="both", expand=True)
        self.build_header(scroll_canvas, is_main=True)
        search_frame = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        search_frame.pack(fill="x", pady=(15, 5), padx=250)
        self.search_entry = ctk.CTkEntry(search_frame, height=45, corner_radius=25, fg_color="#FFFFFF",
                                         border_color="#E2E8F0", border_width=1, font=(self.font_family, 13))
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        self.register_i18n(self.search_entry, "search_placeholder", attr="placeholder_text")
        search_btn = ctk.CTkButton(search_frame, width=100, height=45, corner_radius=25, fg_color="#14142B",
                                   hover_color="#2A2A40", font=(self.font_family, 13, "bold"),
                                   command=self.perform_search)
        search_btn.pack(side="right", padx=(10, 0))
        self.register_i18n(search_btn, "search_btn")
        self.save_btn = ctk.CTkButton(search_frame, width=80, height=45, corner_radius=25, fg_color="#FFFFFF",
                                      border_width=1, border_color="#10B981", text_color="#10B981",
                                      hover_color="#F0FDF4", font=(self.font_family, 13, "bold"),
                                      command=self.save_current_city)
        self.save_btn.pack(side="right", padx=(10, 0))
        self.register_i18n(self.save_btn, "save_btn")
        self.pop_frame = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        self.pop_frame.pack(pady=(0, 20))
        self.update_popular_cities()
        content_wrapper = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        content_wrapper.pack(fill="both", expand=True, padx=80)
        main_card = ctk.CTkFrame(content_wrapper, height=280, corner_radius=20, fg_color="#58627A")
        main_card.pack(fill="x", pady=10)
        main_card.pack_propagate(False)
        text_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        text_frame.pack(side="left", anchor="w", padx=40, pady=20)
        self.ui_city_lbl = ctk.CTkLabel(text_frame, text=self.current_city, font=(self.font_family, 28, "bold"),
                                        text_color="#FFFFFF")
        self.ui_city_lbl.pack(anchor="w")

        date_str = self.get_localized_date_long(datetime.datetime.now())
        self.main_date_lbl = ctk.CTkLabel(text_frame, text=date_str, font=(self.font_family, 12), text_color="#E2E8F0")
        self.main_date_lbl.pack(anchor="w", pady=(0, 20))

        temp_frame = ctk.CTkFrame(text_frame, fg_color="transparent")
        temp_frame.pack(anchor="w")
        self.ui_temp_lbl = ctk.CTkLabel(temp_frame, text="--", font=(self.font_family, 64, "bold"),
                                        text_color="#FFFFFF")
        self.ui_temp_lbl.pack(side="left")
        ctk.CTkLabel(temp_frame, text="°C", font=(self.font_family, 32, "bold"), text_color="#FFFFFF").pack(side="left",
                                                                                                            anchor="n",
                                                                                                            pady=(10,
                                                                                                                  0))
        self.ui_desc_lbl = ctk.CTkLabel(text_frame, text="Loading...", font=(self.font_family, 16),
                                        text_color="#FFFFFF")
        self.ui_desc_lbl.pack(anchor="w")
        self.ui_feels_lbl = ctk.CTkLabel(text_frame, text="--", font=(self.font_family, 12), text_color="#CBD5E1")
        self.ui_feels_lbl.pack(anchor="w")
        cloud_canvas = ctk.CTkCanvas(main_card, width=150, height=100, bg="#58627A", highlightthickness=0)
        cloud_canvas.pack(side="right", padx=50)
        cloud_canvas.create_arc(30, 50, 70, 90, start=90, extent=180, outline="#FFFFFF", width=4, style="arc")
        cloud_canvas.create_arc(50, 20, 110, 80, start=0, extent=180, outline="#FFFFFF", width=4, style="arc")
        cloud_canvas.create_arc(90, 50, 130, 90, start=-90, extent=180, outline="#FFFFFF", width=4, style="arc")
        cloud_canvas.create_line(50, 90, 110, 90, fill="#FFFFFF", width=4)
        grid_frame = ctk.CTkFrame(content_wrapper, fg_color="transparent")
        grid_frame.pack(fill="x", pady=15)
        for i in range(6): grid_frame.grid_columnconfigure(i, weight=1)
        metrics = [
            {"t_key": "humidity", "v": "--%", "c": "#3B82F6", "i": "💧"},
            {"t_key": "wind_speed", "v": "-- km/h", "c": "#10B981", "i": "💨"},
            {"t_key": "visibility", "v": "-- km", "c": "#8B5CF6", "i": "👁"},
            {"t_key": "pressure", "v": "-- mb", "c": "#F59E0B", "i": "⏱"},
            {"t_key": "dew_point", "v": "--°C", "c": "#EC4899", "i": "🌡"},
            {"t_key": "uv_index", "v": "--", "c": "#EF4444", "i": "☀"}
        ]
        self.ui_metric_vals = []
        for idx, m in enumerate(metrics):
            card = ctk.CTkFrame(grid_frame, fg_color="#FFFFFF", height=110, corner_radius=16)
            card.grid(row=0, column=idx, sticky="ew", padx=8)
            card.pack_propagate(False)
            icon_bg = ctk.CTkFrame(card, fg_color=m["c"], width=32, height=32, corner_radius=10)
            icon_bg.pack(anchor="w", padx=15, pady=(15, 10))
            icon_bg.pack_propagate(False)
            ctk.CTkLabel(icon_bg, text=m["i"], text_color="#FFFFFF", font=(self.font_family, 16)).place(relx=0.5,
                                                                                                        rely=0.5,
                                                                                                        anchor="center")
            lbl_title = ctk.CTkLabel(card, font=(self.font_family, 12), text_color="#6E7191")
            lbl_title.pack(anchor="w", padx=15)
            self.register_i18n(lbl_title, m["t_key"])
            val_lbl = ctk.CTkLabel(card, text=m["v"], font=(self.font_family, 16, "bold"), text_color="#14142B")
            val_lbl.pack(anchor="w", padx=15)
            self.ui_metric_vals.append(val_lbl)
        chart_card = ctk.CTkFrame(content_wrapper, fg_color="#FFFFFF", corner_radius=20, height=270)
        chart_card.pack(fill="x", pady=15)
        chart_card.pack_propagate(False)
        chart_title = ctk.CTkLabel(chart_card, font=(self.font_family, 16, "bold"), text_color="#14142B")
        chart_title.pack(anchor="w", padx=25, pady=(20, 10))
        self.register_i18n(chart_title, "todays_temp")
        self.chart_scroll = ctk.CTkScrollableFrame(chart_card, fg_color="transparent", orientation="horizontal",
                                                   height=180)
        self.chart_scroll.pack(fill="x", padx=10, pady=(0, 10))

        # ==========================================
        # 7-DAY FORECAST (DYNAMIC DAYS BUGFIX)
        # ==========================================
        forecast_card = ctk.CTkFrame(content_wrapper, fg_color="#FFFFFF", corner_radius=20)
        forecast_card.pack(fill="x", pady=15, ipady=10)
        forecast_title = ctk.CTkLabel(forecast_card, font=(self.font_family, 16, "bold"), text_color="#14142B")
        forecast_title.pack(anchor="w", padx=25, pady=(20, 15))
        self.register_i18n(forecast_title, "7day_forecast")

        start_date = datetime.date.today()

        wd_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        wd_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        wd_kg = ["Дүйшөмбү", "Шейшемби", "Шаршемби", "Бейшемби", "Жума", "Ишемби", "Жекшемби"]

        desc_trans = {
            "Sunny": {"EN": "Sunny", "RU": "Солнечно", "KG": "Күн ачык"},
            "Partly Cloudy": {"EN": "Partly Cloudy", "RU": "Переменная облачность", "KG": "Анда-санда булуттуу"},
            "Cloudy": {"EN": "Cloudy", "RU": "Облачно", "KG": "Булуттуу"},
            "Rainy": {"EN": "Rainy", "RU": "Дождь", "KG": "Жамгыр"}
        }

        templates = [
            ("☼", "Sunny", "15°", "25°", "#FBBF24", "#F59E0B", "#EAB308"),
            ("☁", "Partly Cloudy", "14°", "22°", "#60A5FA", "#FBBF24", "#6E7191"),
            ("☁", "Cloudy", "12°", "20°", "#9CA3AF", "#D1D5DB", "#6E7191"),
            ("🌧", "Rainy", "10°", "18°", "#3B82F6", "#60A5FA", "#3B82F6"),
            ("☁", "Partly Cloudy", "13°", "21°", "#60A5FA", "#FBBF24", "#6E7191"),
            ("☼", "Sunny", "14°", "24°", "#FBBF24", "#F59E0B", "#EAB308"),
            ("☼", "Sunny", "16°", "26°", "#FBBF24", "#F59E0B", "#EAB308")
        ]

        self.forecast_rows = []
        for idx in range(7):
            current_day_obj = start_date + datetime.timedelta(days=idx)
            w_idx = current_day_obj.weekday()

            if self.current_lang == "RU":
                day_name = wd_ru[w_idx]
            elif self.current_lang == "KG":
                day_name = wd_kg[w_idx]
            else:
                day_name = wd_en[w_idx]

            d_ico, base_desc, d_min, d_max, c1, c2, ico_col = templates[idx]
            d_desc = desc_trans[base_desc].get(self.current_lang, base_desc)

            if self.temp_unit == "F":
                t_min_int = int(d_min.replace("°", ""))
                t_max_int = int(d_max.replace("°", ""))
                d_min = f"{int(t_min_int * 9 / 5 + 32)}°"
                d_max = f"{int(t_max_int * 9 / 5 + 32)}°"

            row = ctk.CTkFrame(forecast_card, fg_color="transparent", height=45)
            row.pack(fill="x", padx=25)
            row.pack_propagate(False)

            day_lbl = ctk.CTkLabel(row, text=day_name, font=(self.font_family, 14), text_color="#14142B", width=120,
                                   anchor="w")
            day_lbl.pack(side="left")
            icon_lbl = ctk.CTkLabel(row, text=d_ico, font=(self.font_family, 18), text_color=ico_col, width=30,
                                    anchor="w")
            icon_lbl.pack(side="left")
            desc_lbl = ctk.CTkLabel(row, text=d_desc, font=(self.font_family, 14), text_color="#6E7191", width=150,
                                    anchor="w")
            desc_lbl.pack(side="left")
            max_lbl = ctk.CTkLabel(row, text=d_max, font=(self.font_family, 14, "bold"), text_color="#14142B",
                                   anchor="e", width=40)
            max_lbl.pack(side="right")
            bar_lbl = self.create_rounded_gradient_bar(row, 100, 6, c1, c2)
            bar_lbl.pack(side="right", padx=15, pady=20)
            min_lbl = ctk.CTkLabel(row, text=d_min, font=(self.font_family, 14), text_color="#A0AEC0", anchor="w",
                                   width=40)
            min_lbl.pack(side="right")

            self.forecast_rows.append({
                "day_lbl": day_lbl, "icon_lbl": icon_lbl, "desc_lbl": desc_lbl,
                "max_lbl": max_lbl, "min_lbl": min_lbl, "bar_lbl": bar_lbl,
                "base_desc": base_desc
            })

        self.apply_language()
        self.fetch_weather(self.current_city)

    def save_current_city(self):
        if not hasattr(self, 'current_city_data'): return
        for c in self.saved_cities:
            if c["name"] == self.current_city_data["name"]: return
        now_str = datetime.datetime.now().strftime("Saved %m/%d/%Y")
        new_city = self.current_city_data.copy()
        new_city["date"] = now_str
        self.saved_cities.append(new_city)
        if hasattr(self, 'save_btn'):
            self.save_btn.configure(text=self.get_text("saved_btn"))
            for item in self.dynamic_labels:
                if item["widget"] == self.save_btn: item["key"] = "saved_btn"

    # ==========================================
    # API FETCHING LOGIC
    # ==========================================
    def perform_search(self):
        city = self.search_entry.get().strip()
        if city: self.fetch_weather(city)

    def fetch_weather(self, city_name, target_date=None):
        self.current_city = city_name
        if target_date is None:
            target_date = datetime.datetime.now()

        today = datetime.date.today()
        target_day = target_date.date()
        delta_days = (target_day - today).days

        if self.current_lang == "RU":
            sunny_desc = "Солнечно"
        elif self.current_lang == "KG":
            sunny_desc = "Күн ачык"
        else:
            sunny_desc = "Sunny"

        day_seed = target_date.day + len(city_name)
        mock_temp = 20 + (day_seed % 7)
        mock_feels = mock_temp - 1
        mock_humidity = 50 + (day_seed % 15)
        mock_wind = 2.5 + (day_seed % 4) * 0.5
        mock_pressure = 1011 + (day_seed % 6)

        if self.temp_unit == "F":
            mock_temp = int(mock_temp * 9 / 5 + 32)
            mock_feels = int(mock_feels * 9 / 5 + 32)

        fallback_data = {
            'main': {
                'temp': mock_temp,
                'feels_like': mock_feels,
                'humidity': mock_humidity,
                'pressure': mock_pressure
            },
            'weather': [{'description': sunny_desc}],
            'wind': {'speed': mock_wind},
            'visibility': 10000
        }

        if 0 <= delta_days <= 4 and OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "YOUR_API_KEY_HERE":
            try:
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(city_name)}&limit=1&appid={OPENWEATHER_API_KEY}"
                req = urllib.request.urlopen(geo_url, timeout=4)
                geo_data = json.loads(req.read())

                if geo_data:
                    lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
                    name = geo_data[0]['name']

                    units = "metric" if self.temp_unit == "C" else "imperial"
                    lang_param = "ru" if self.current_lang in ["RU", "KG"] else "en"

                    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units={units}&lang={lang_param}"
                    w_req = urllib.request.urlopen(weather_url, timeout=4)
                    w_data = json.loads(w_req.read())

                    target_date_str = target_date.strftime("%Y-%m-%d")
                    match_item = None

                    for item in w_data.get('list', []):
                        if item.get('dt_txt', '').startswith(target_date_str):
                            if "12:00:00" in item.get('dt_txt', ''):
                                match_item = item
                                break
                            if match_item is None:
                                match_item = item

                    if match_item:
                        self.update_weather_ui_live(name, match_item)
                        self.update_forecast_ui(w_data.get('list', []))
                        self.update_hourly_ui(w_data.get('list', []))
                        return
                    elif w_data.get('list'):
                        self.update_weather_ui_live(name, w_data['list'][0])
                        self.update_forecast_ui(w_data.get('list', []))
                        self.update_hourly_ui(w_data.get('list', []))
                        return
            except Exception as e:
                print("Сеть недоступна:", e)

        self.update_weather_ui_live(city_name.capitalize(), fallback_data)

    def update_weather_ui_live(self, city_name, current_data):
        self.ui_city_lbl.configure(text=city_name)
        if hasattr(self, 'cal_city_lbl'): self.cal_city_lbl.configure(text=city_name)
        if hasattr(self, 'header_city_lbl'): self.header_city_lbl.configure(text=city_name)

        if hasattr(self, 'save_btn'):
            is_saved = any(c["name"] == city_name for c in self.saved_cities)
            btn_key = "saved_btn" if is_saved else "save_btn"
            self.save_btn.configure(text=self.get_text(btn_key))
            for item in self.dynamic_labels:
                if item["widget"] == self.save_btn: item["key"] = btn_key

        temp = int(current_data['main']['temp'])
        desc = current_data['weather'][0]['description'].capitalize()
        feels_like = int(current_data['main']['feels_like'])

        self.ui_temp_lbl.configure(text=str(temp))
        self.ui_desc_lbl.configure(text=desc)

        feels_str = self.get_text('feels_like')
        self.ui_feels_lbl.configure(text=f"{feels_str} {feels_like}°{self.temp_unit}")

        humidity = current_data['main']['humidity']
        wind_speed = current_data['wind']['speed']
        visibility = current_data.get('visibility', 10000) / 1000
        pressure = current_data['main']['pressure']

        unit_str = "m/s" if self.temp_unit == "C" else "mph"
        self.ui_metric_vals[0].configure(text=f"{humidity}%")
        self.ui_metric_vals[1].configure(text=f"{wind_speed} {unit_str}")
        self.ui_metric_vals[2].configure(text=f"{visibility:.1f} km")
        self.ui_metric_vals[3].configure(text=f"{pressure} hPa")

        self.current_city_data = {
            "name": city_name, "t": f"{temp}°", "desc": desc,
            "feels_like": f"{feels_like}°", "humidity": f"{humidity}%", "wind": f"{wind_speed} {unit_str}"
        }

    def update_forecast_ui(self, forecast_list):
        if not hasattr(self, 'forecast_rows'): return
        import random

        daily_data = {}
        for item in forecast_list:
            dt_txt = item.get('dt_txt', '')
            if not dt_txt: continue
            date_str = dt_txt.split(' ')[0]
            if date_str not in daily_data:
                daily_data[date_str] = {
                    'temps': [],
                    'weather_main': item['weather'][0]['main'],
                    'weather_desc': item['weather'][0]['description']
                }
            daily_data[date_str]['temps'].append(item['main']['temp'])
            if "12:00:00" in dt_txt:
                daily_data[date_str]['weather_main'] = item['weather'][0]['main']
                daily_data[date_str]['weather_desc'] = item['weather'][0]['description']

        start_date = datetime.date.today()

        last_max = 20
        last_min = 10

        desc_trans = {
            "Sunny": {"EN": "Sunny", "RU": "Солнечно", "KG": "Күн ачык"},
            "Partly Cloudy": {"EN": "Partly Cloudy", "RU": "Переменная облачность", "KG": "Анда-санда булуттуу"},
            "Cloudy": {"EN": "Cloudy", "RU": "Облачно", "KG": "Булуттуу"},
            "Rainy": {"EN": "Rainy", "RU": "Дождь", "KG": "Жамгыр"}
        }

        for idx in range(7):
            if idx >= len(self.forecast_rows): break
            current_day_obj = start_date + datetime.timedelta(days=idx)
            date_str = current_day_obj.strftime("%Y-%m-%d")
            row_widgets = self.forecast_rows[idx]

            if date_str in daily_data:
                temps = daily_data[date_str]['temps']
                t_min = min(temps)
                t_max = max(temps)
                w_main = daily_data[date_str]['weather_main']
                last_max = t_max
                last_min = t_min
            else:
                t_max = last_max + random.randint(-2, 2)
                t_min = last_min + random.randint(-2, 2)
                if t_min > t_max: t_min, t_max = t_max, t_min
                w_main = random.choice(["Clear", "Clouds", "Rain"])
                last_max = t_max
                last_min = t_min

            w_main_lower = w_main.lower()
            if "clear" in w_main_lower:
                base_desc = "Sunny"
                d_ico = "☼"
                ico_col = "#EAB308"
                c1, c2 = "#FBBF24", "#F59E0B"
            elif any(x in w_main_lower for x in ["rain", "drizzle", "thunderstorm"]):
                base_desc = "Rainy"
                d_ico = "🌧"
                ico_col = "#3B82F6"
                c1, c2 = "#3B82F6", "#60A5FA"
            elif "cloud" in w_main_lower:
                base_desc = "Cloudy" if w_main_lower == "clouds" else "Partly Cloudy"
                d_ico = "☁"
                ico_col = "#6E7191"
                c1, c2 = "#9CA3AF", "#D1D5DB"
            else:
                base_desc = "Partly Cloudy"
                d_ico = "☁"
                ico_col = "#6E7191"
                c1, c2 = "#60A5FA", "#FBBF24"

            d_desc = desc_trans.get(base_desc, desc_trans["Partly Cloudy"]).get(self.current_lang, base_desc)

            row_widgets['icon_lbl'].configure(text=d_ico, text_color=ico_col)
            row_widgets['desc_lbl'].configure(text=d_desc)
            row_widgets['min_lbl'].configure(text=f"{int(t_min)}°")
            row_widgets['max_lbl'].configure(text=f"{int(t_max)}°")

            new_img = self.get_gradient_bar_image(100, 6, c1, c2)
            row_widgets['bar_lbl'].configure(image=new_img)

    def update_hourly_ui(self, forecast_list):
        if not hasattr(self, 'chart_scroll'): return

        for widget in self.chart_scroll.winfo_children():
            widget.destroy()

        items = forecast_list[:12]
        if not items: return

        temps = [item['main']['temp'] for item in items]
        min_t = min(temps)
        max_t = max(temps)
        diff = max_t - min_t if max_t != min_t else 1

        for item in items:
            t_val = item['main']['temp']
            dt_txt = item.get('dt_txt', '')
            if not dt_txt: continue

            time_str = dt_txt.split(' ')[1][:5]
            h_temp = f"{int(t_val)}°"
            h_height = int(30 + ((t_val - min_t) / diff) * 50)

            w_main_lower = item['weather'][0]['main'].lower()
            if "clear" in w_main_lower:
                h_icon = "☼"
            elif any(x in w_main_lower for x in ["rain", "drizzle", "thunderstorm"]):
                h_icon = "🌧"
            elif "cloud" in w_main_lower:
                h_icon = "☁"
            else:
                h_icon = "☁"

            col = ctk.CTkFrame(self.chart_scroll, fg_color="transparent", width=55)
            col.pack(side="left", fill="y", padx=5)
            col.pack_propagate(False)
            ctk.CTkLabel(col, text=h_temp, font=(self.font_family, 12, "bold"), text_color="#6E7191").pack(side="top")
            bar_container = ctk.CTkFrame(col, fg_color="transparent", height=100)
            bar_container.pack(side="top", pady=5)
            bar_container.pack_propagate(False)
            bar_lbl = self.create_rounded_gradient_bar(bar_container, 28, h_height, "#563BFE", "#3BA6FF")
            bar_lbl.pack(side="bottom")
            ctk.CTkLabel(col, text=h_icon, font=(self.font_family, 16), text_color="#A0AEC0").pack(side="top",
                                                                                                   pady=(0, 2))
            ctk.CTkLabel(col, text=time_str, font=(self.font_family, 10), text_color="#A0AEC0").pack(side="top")

    # ==========================================
    # SCREEN 2 & 3: SAVED CITIES & SETTINGS
    # ==========================================
    def show_saved_cities_screen(self):
        self.current_screen = "saved"
        self.clear_screen()
        if self.menu_visible: self.toggle_menu()
        scroll_canvas = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll_canvas.pack(fill="both", expand=True)
        self.build_header(scroll_canvas, is_main=False, title_text="saved_title")
        btn_frame = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 20))
        export_btn = ctk.CTkButton(btn_frame, font=(self.font_family, 13, "bold"), fg_color="#10B981",
                                   hover_color="#059669", height=40, corner_radius=10, width=180)
        export_btn.pack(anchor="center")
        self.register_i18n(export_btn, "export_btn")
        grid_frame = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        grid_frame.pack(fill="x", padx=80, pady=10)
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        if not self.saved_cities:
            ctk.CTkLabel(grid_frame, text="No saved cities yet.", font=(self.font_family, 16),
                         text_color="#A0AEC0").grid(row=0, column=0, columnspan=2, pady=50)
        for idx, city in enumerate(self.saved_cities):
            r, c = idx // 2, idx % 2
            card_bg, element_bg, hover_bg = ("#314BF5", "#4B63F6", "#5B73F6") if idx % 2 == 0 else ("#2BB0FE",
                                                                                                    "#4CBFF6",
                                                                                                    "#5CCFF6")
            card = ctk.CTkFrame(grid_frame, fg_color=card_bg, height=250, corner_radius=20)
            card.grid(row=r, column=c, sticky="ew", padx=15, pady=15)
            card.pack_propagate(False)
            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=25, pady=(15, 5))
            title_box = ctk.CTkFrame(top_row, fg_color="transparent")
            title_box.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(title_box, text=city["name"], font=(self.font_family, 24, "bold"), text_color="#FFFFFF").pack(
                anchor="w")
            ctk.CTkLabel(title_box, text=city["date"], font=(self.font_family, 12), text_color="#D1D5DB").pack(
                anchor="w")
            btn_box = ctk.CTkFrame(top_row, fg_color="transparent")
            btn_box.pack(side="right", anchor="n")
            ctk.CTkButton(btn_box, text="⬇", width=35, height=35, corner_radius=10, fg_color=element_bg,
                          hover_color=hover_bg, text_color="#FFFFFF", font=("", 16)).pack(side="left", padx=8)
            ctk.CTkButton(btn_box, text="🗑", width=35, height=35, corner_radius=10, fg_color=element_bg,
                          hover_color=hover_bg, text_color="#FFFFFF", font=("", 16), command=lambda n=city["name"]: [
                    setattr(self, 'saved_cities', [x for x in self.saved_cities if x["name"] != n]),
                    self.show_saved_cities_screen()]).pack(side="left")
            temp_row = ctk.CTkFrame(card, fg_color="transparent")
            temp_row.pack(anchor="w", padx=25, pady=(0, 10))
            ctk.CTkLabel(temp_row, text=city["t"], font=(self.font_family, 56, "bold"), text_color="#FFFFFF").pack(
                side="left")
            ctk.CTkLabel(temp_row, text=city["desc"], font=(self.font_family, 18), text_color="#FFFFFF").pack(
                side="left", padx=15, pady=(15, 0), anchor="s")
            metrics_box = ctk.CTkFrame(card, fg_color="transparent")
            metrics_box.pack(fill="x", padx=25)
            for i in range(3): metrics_box.grid_columnconfigure(i, weight=1)
            m_data = [("🌡", "Feels Like", city.get("feels_like", "--")), ("💧", "Humidity", city.get("humidity", "--")),
                      ("💨", "Wind", city.get("wind", "--"))]
            for m_idx, (m_i, m_t, m_v) in enumerate(m_data):
                m_frame = ctk.CTkFrame(metrics_box, fg_color=element_bg, corner_radius=12, height=90)
                m_frame.grid(row=0, column=m_idx, sticky="ew", padx=6)
                m_frame.pack_propagate(False)
                ctk.CTkLabel(m_frame, text=m_i, font=(self.font_family, 18), text_color="#FFFFFF").pack(anchor="w",
                                                                                                        padx=15,
                                                                                                        pady=(6, 0))
                ctk.CTkLabel(m_frame, text=m_t, font=(self.font_family, 11), text_color="#D1D5DB").pack(anchor="w",
                                                                                                        padx=15,
                                                                                                        pady=(0, 0))
                ctk.CTkLabel(m_frame, text=m_v, font=(self.font_family, 15, "bold"), text_color="#FFFFFF").pack(
                    anchor="w", padx=15, pady=(0, 0))
        self.apply_language()

    def show_settings_screen(self):
        self.current_screen = "settings"
        self.clear_screen()
        if self.menu_visible: self.toggle_menu()
        scroll_canvas = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll_canvas.pack(fill="both", expand=True)
        self.build_header(scroll_canvas, is_main=False, title_text="settings_title")
        content_wrapper = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        content_wrapper.pack(fill="both", expand=True, padx=250, pady=10)
        disp_card = ctk.CTkFrame(content_wrapper, fg_color="#FFFFFF", corner_radius=16)
        disp_card.pack(fill="x", pady=10, ipady=10)
        lbl = ctk.CTkLabel(disp_card, font=(self.font_family, 16, "bold"), text_color="#14142B")
        lbl.pack(anchor="w", padx=25, pady=(20, 10))
        self.register_i18n(lbl, "display")
        self.build_setting_row(disp_card, "temp_unit", "temp_unit_desc", widget_type="toggle_cf")
        self.build_setting_row(disp_card, "dark_mode", "dark_mode_desc", widget_type="switch", state="disabled")
        notif_card = ctk.CTkFrame(content_wrapper, fg_color="#FFFFFF", corner_radius=16)
        notif_card.pack(fill="x", pady=10, ipady=10)
        lbl2 = ctk.CTkLabel(notif_card, font=(self.font_family, 16, "bold"), text_color="#14142B")
        lbl2.pack(anchor="w", padx=25, pady=(20, 10))
        self.register_i18n(lbl2, "notifications")
        self.build_setting_row(notif_card, "weather_alerts", "weather_alerts_desc", widget_type="switch")
        loc_card = ctk.CTkFrame(content_wrapper, fg_color="#FFFFFF", corner_radius=16)
        loc_card.pack(fill="x", pady=10, ipady=10)
        lbl3 = ctk.CTkLabel(loc_card, font=(self.font_family, 16, "bold"), text_color="#14142B")
        lbl3.pack(anchor="w", padx=25, pady=(20, 10))
        self.register_i18n(lbl3, "location")
        self.build_setting_row(loc_card, "auto_detect", "auto_detect_desc", widget_type="switch", icon="📍")
        self.apply_language()

    def build_setting_row(self, parent, title_key, desc_key, widget_type, state="normal", icon=None):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=25, pady=10)
        text_col = ctk.CTkFrame(row, fg_color="transparent")
        text_col.pack(side="left")
        if icon:
            icon_box = ctk.CTkFrame(text_col, fg_color="#563BFE", width=30, height=30, corner_radius=8)
            icon_box.pack(side="left", padx=(0, 15));
            icon_box.pack_propagate(False)
            ctk.CTkLabel(icon_box, text=icon, text_color="#FFFFFF", font=("", 14)).place(relx=0.5, rely=0.5,
                                                                                         anchor="center")
        text_inner = ctk.CTkFrame(text_col, fg_color="transparent")
        text_inner.pack(side="left")
        title_lbl = ctk.CTkLabel(text_inner, font=(self.font_family, 14, "bold"),
                                 text_color="#14142B" if state == "normal" else "#A0AEC0")
        title_lbl.pack(anchor="w");
        self.register_i18n(title_lbl, title_key)
        desc_lbl = ctk.CTkLabel(text_inner, font=(self.font_family, 11), text_color="#A0AEC0")
        desc_lbl.pack(anchor="w");
        self.register_i18n(desc_lbl, desc_key)
        if widget_type == "switch":
            sw = ctk.CTkSwitch(row, text="", progress_color="#563BFE", width=50)
            sw.pack(side="right")
            if state == "disabled": sw.configure(state="disabled")
        elif widget_type == "toggle_cf":
            btn_box = ctk.CTkFrame(row, fg_color="#F5F7FB", corner_radius=10, height=36)
            btn_box.pack(side="right")
            c_btn = ctk.CTkButton(btn_box, text="°C", width=40, height=30, corner_radius=8,
                                  font=(self.font_family, 12, "bold"),
                                  fg_color="#563BFE" if self.temp_unit == "C" else "transparent",
                                  text_color="#FFFFFF" if self.temp_unit == "C" else "#6E7191",
                                  hover_color="#4A2EE0" if self.temp_unit == "C" else "#E2E8F0")
            c_btn.pack(side="left", padx=3, pady=3)
            f_btn = ctk.CTkButton(btn_box, text="°F", width=40, height=30, corner_radius=8,
                                  font=(self.font_family, 12, "bold"),
                                  fg_color="#563BFE" if self.temp_unit == "F" else "transparent",
                                  text_color="#FFFFFF" if self.temp_unit == "F" else "#6E7191",
                                  hover_color="#4A2EE0" if self.temp_unit == "F" else "transparent")
            f_btn.pack(side="left", padx=(0, 3), pady=3)
            c_btn.configure(command=lambda: [setattr(self, 'temp_unit', "C"),
                                             c_btn.configure(fg_color="#563BFE", text_color="#FFFFFF"),
                                             f_btn.configure(fg_color="transparent", text_color="#6E7191"),
                                             self.show_main_screen()])
            f_btn.configure(command=lambda: [setattr(self, 'temp_unit', "F"),
                                             f_btn.configure(fg_color="#563BFE", text_color="#FFFFFF"),
                                             c_btn.configure(fg_color="transparent", text_color="#6E7191"),
                                             self.show_main_screen()])


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()