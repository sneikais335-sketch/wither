# Техническое задание: Weather Forecast Desktop Application
### Для ИИ-агента разработки | Версия 1.0 | Май 2026

---

## 1. ОБЩИЙ ОБЗОР ПРОЕКТА

**Название:** Weather Forecast App  
**Платформа:** Desktop (Windows / macOS / Linux)  
**Технология интерфейса:** CustomTkinter (Python)  
**База данных:** SQLite (локальная, встроенная)  
**API погоды:** OpenWeatherMap (https://openweathermap.org)  
**Иконка приложения:** предоставлена пользователем (файл `photo_5429185189155376072_y.jpg` → конвертировать в `.ico` / `.icns`)

---

## 2. АРХИТЕКТУРА ПРОЕКТА

```
weather_app/
├── main.py                  # Точка входа, инициализация приложения
├── app.py                   # Главный класс App (CTk root window)
├── config.py                # Константы: цвета, шрифты, API_KEY, размеры
├── assets/
│   ├── icon.ico             # Иконка приложения (Windows)
│   ├── icon.icns            # Иконка приложения (macOS)
│   └── icon.png             # Иконка приложения (Linux / общая)
├── database/
│   ├── db_manager.py        # Менеджер SQLite подключений
│   ├── cities_db.py         # CRUD для таблицы saved_cities
│   ├── forecast_db.py       # CRUD для таблицы weekly_forecast
│   └── calendar_db.py       # CRUD для таблицы calendar_events
├── api/
│   ├── weather_api.py       # Запросы к OpenWeatherMap
│   └── parser.py            # Парсинг и нормализация ответов API
├── views/
│   ├── main_view.py         # Главный экран (прогноз для текущего города)
│   ├── saved_cities_view.py # Экран «Сохранённые города»
│   ├── settings_view.py     # Экран настроек
│   ├── calendar_view.py     # Виджет / попап календаря
│   └── menu_panel.py        # Боковая панель (Menu)
├── components/
│   ├── weather_card.py      # Главная карточка (город, температура, иконка)
│   ├── stat_tile.py         # Плитки статистики (Humidity, Wind и т.д.)
│   ├── hourly_chart.py      # График почасовой температуры (Canvas)
│   ├── weekly_row.py        # Строка 7-дневного прогноза
│   ├── city_card.py         # Карточка сохранённого города
│   └── export_dialog.py     # Диалог экспорта (JSON / CSV / Excel)
├── i18n/
│   ├── en.json              # Английские строки интерфейса
│   ├── ru.json              # Русские строки интерфейса
│   └── kg.json              # Кыргызские строки интерфейса
└── utils/
    ├── language.py          # Менеджер языков (load / switch)
    ├── exporter.py          # Логика экспорта данных
    └── helpers.py           # Вспомогательные функции (дата, конвертация)
```

---

## 3. БАЗА ДАННЫХ SQLite

**Файл БД:** `weather_app.db` (создаётся автоматически при первом запуске)

### 3.1 Таблица: `saved_cities`
Хранит города, добавленные пользователем.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Уникальный ID |
| `name` | TEXT NOT NULL | Название города |
| `country` | TEXT | Код страны (RU, KG, US…) |
| `lat` | REAL | Широта |
| `lon` | REAL | Долгота |
| `saved_at` | TEXT | Дата добавления (ISO формат) |

### 3.2 Таблица: `weekly_forecast`
Кэш прогноза на 7 дней для каждого города.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Уникальный ID |
| `city_name` | TEXT NOT NULL | Название города |
| `date` | TEXT NOT NULL | Дата (YYYY-MM-DD) |
| `day_name` | TEXT | Название дня (Monday…) |
| `condition` | TEXT | Описание погоды (Sunny, Rainy…) |
| `icon_code` | TEXT | Код иконки OWM (01d, 02d…) |
| `temp_min` | REAL | Минимальная температура (°C) |
| `temp_max` | REAL | Максимальная температура (°C) |
| `humidity` | INTEGER | Влажность (%) |
| `wind_speed` | REAL | Скорость ветра (км/ч) |
| `pressure` | INTEGER | Давление (мб) |
| `visibility` | REAL | Видимость (км) |
| `dew_point` | REAL | Точка росы (°C) |
| `uv_index` | REAL | УФ-индекс |
| `cached_at` | TEXT | Время кэширования |

### 3.3 Таблица: `hourly_forecast`
Кэш почасового прогноза (для графика «Today's Temperature»).

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Уникальный ID |
| `city_name` | TEXT NOT NULL | Название города |
| `datetime` | TEXT NOT NULL | Дата и время (ISO) |
| `temp` | REAL | Температура (°C) |
| `condition` | TEXT | Описание погоды |
| `icon_code` | TEXT | Код иконки OWM |
| `cached_at` | TEXT | Время кэширования |

### 3.4 Таблица: `calendar_events`
События, привязанные к датам (из виджета календаря).

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Уникальный ID |
| `date` | TEXT NOT NULL | Дата события (YYYY-MM-DD) |
| `title` | TEXT NOT NULL | Заголовок события |
| `note` | TEXT | Доп. заметка |
| `created_at` | TEXT | Дата создания |

### 3.5 Таблица: `app_settings`
Настройки приложения (одна строка).

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Всегда = 1 |
| `language` | TEXT | Язык: `en`, `ru`, `kg` |
| `temp_unit` | TEXT | Единица: `C` или `F` |
| `default_city` | TEXT | Город по умолчанию |
| `notifications_enabled` | INTEGER | 1 / 0 (bool) |
| `auto_location` | INTEGER | 1 / 0 (bool) |

---

## 4. ДИЗАЙН-СИСТЕМА (CustomTkinter)

> Все размеры фиксированы. При переходе в полноэкранный режим размеры иконок, карточек и элементов НЕ масштабируются. Используется `place()` или `pack()`/`grid()` с фиксированными `width` и `height`.

### 4.1 Цветовая палитра (точное соответствие дизайну)

```python
# config.py — COLORS
COLORS = {
    # Фон страницы
    "bg_page":         "#E8EEF7",   # светло-голубоватый фон (основной)
    "bg_card":         "#FFFFFF",   # белые карточки
    "bg_main_card":    "#6B7B94",   # тёмно-серая главная карточка (город+погода)

    # Акцентные цвета — заголовок «Weather Forecast»
    "accent_blue":     "#4A7AE8",   # «Weather» (синий)
    "accent_purple":   "#8B5CF6",   # «Forecast» (фиолетовый)

    # Меню (боковая панель)
    "menu_header_bg":  "#7C3AED",   # градиент от синего к фиолетовому (верх меню)
    "menu_header_bg2": "#3B82F6",   # (низ градиента)
    "menu_item_bg":    "#F3F4F6",   # фон пункта меню
    "menu_item_hover": "#E5E7EB",

    # Плитки статистики (иконки)
    "icon_humidity":   "#3B82F6",   # синий (Humidity)
    "icon_wind":       "#10B981",   # зелёный (Wind Speed)
    "icon_visibility": "#8B5CF6",   # фиолетовый (Visibility)
    "icon_pressure":   "#F97316",   # оранжевый (Pressure)
    "icon_dew":        "#EC4899",   # розовый (Dew Point)
    "icon_uv":         "#EAB308",   # жёлтый (UV Index)

    # График температуры
    "chart_bar":       "#93C5FD",   # светло-синий столбик
    "chart_bar_tall":  "#3B82F6",   # тёмно-синий для высоких столбиков

    # 7-Day Forecast — температурная полоса
    "temp_bar_cold":   "#86EFAC",   # зелёная (мин. температура)
    "temp_bar_hot":    "#FDE047",   # жёлтая (макс. температура)

    # Карточки сохранённых городов
    "city_card_bg":    "#3730A3",   # тёмно-синий/фиолетовый
    "city_card_sub":   "#4F46E5",   # оттенок плиток внутри карточки

    # Кнопка «Search»
    "btn_search_bg":   "#111827",   # почти чёрный
    "btn_search_text": "#FFFFFF",

    # Текст
    "text_primary":    "#111827",
    "text_secondary":  "#6B7280",
    "text_white":      "#FFFFFF",
    "text_link":       "#3B82F6",   # цвет популярных городов-ссылок
}
```

### 4.2 Шрифты

```python
FONTS = {
    "title_large":  ("Segoe UI", 32, "bold"),     # «Weather Forecast»
    "subtitle":     ("Segoe UI", 12, "normal"),   # подзаголовок
    "temp_big":     ("Segoe UI", 42, "bold"),     # большая температура
    "temp_unit":    ("Segoe UI", 22, "normal"),   # «°C»
    "city_name":    ("Segoe UI", 20, "bold"),     # название города
    "date_text":    ("Segoe UI", 11, "normal"),   # дата
    "condition":    ("Segoe UI", 16, "normal"),   # «Partly Cloudy»
    "feels_like":   ("Segoe UI", 11, "normal"),   # «Feels like 16°C»
    "stat_label":   ("Segoe UI", 11, "normal"),   # «Humidity»
    "stat_value":   ("Segoe UI", 14, "bold"),     # «65%»
    "chart_temp":   ("Segoe UI", 10, "normal"),   # температура на графике
    "week_day":     ("Segoe UI", 13, "normal"),   # «Monday»
    "week_cond":    ("Segoe UI", 13, "normal"),   # «Sunny»
    "section_head": ("Segoe UI", 16, "bold"),     # «Today's Temperature»
    "search_input": ("Segoe UI", 13, "normal"),   # поле поиска
    "btn_text":     ("Segoe UI", 13, "bold"),     # кнопки
    "menu_title":   ("Segoe UI", 22, "bold"),     # «Menu»
    "menu_sub":     ("Segoe UI", 12, "normal"),   # подзаголовок меню
}
```

### 4.3 Фиксированные размеры элементов

```python
SIZES = {
    "window_default":   (1100, 850),  # размер окна по умолчанию
    "window_min":       (900, 700),   # минимальный размер

    # Статистические плитки
    "stat_tile_w":      130,
    "stat_tile_h":      90,
    "stat_icon_box":    36,           # квадрат иконки (фиксирован)
    "stat_icon_size":   20,           # размер иконки внутри

    # Главная карточка
    "main_card_h":      190,
    "weather_icon_size": 80,          # иконка облако/солнце (ФИКСИРОВАНА)

    # График
    "chart_bar_w":      28,           # ширина столбика (фиксирована)
    "chart_max_h":      80,           # максимальная высота столбика

    # Карточка сохранённого города
    "city_card_w":      300,
    "city_card_h":      180,

    # Боковое меню
    "menu_panel_w":     280,

    # Иконки погоды в 7-day forecast
    "forecast_icon":    28,           # ФИКСИРОВАН
}
```

---

## 5. ЭКРАНЫ И ИХ КОМПОНЕНТЫ

### 5.1 Главный экран (`main_view.py`)

**Компоненты (сверху вниз):**

1. **Хедер** — гамбургер-кнопка (слева), заголовок «Weather Forecast» (синий+фиолетовый), дата с иконкой (справа)
2. **Подзаголовок** — «Your personal weather companion…»
3. **Поисковая строка** — поле ввода + кнопка «Search»; под строкой — ярлыки популярных городов
4. **Главная карточка** — тёмно-серая; слева: название города, дата, большая температура, описание, «Feels like»; справа: SVG-иконка погоды (фиксированный размер 80px)
5. **Строка плиток статистики** — 6 плиток: Humidity, Wind Speed, Visibility, Pressure, Dew Point, UV Index
6. **Секция «Today's Temperature»** — горизонтально прокручиваемый Canvas-график: столбики + температура сверху + иконка условия снизу + время снизу
7. **Секция «7-Day Forecast»** — 7 строк: день, иконка, описание, температурная полоса (min → max), макс. температура

**Поведение:**
- При загрузке — автоматически запрашивает погоду для города по умолчанию (из `app_settings`)
- При поиске — вызов API, обновление всех секций, кэширование в `weekly_forecast` и `hourly_forecast`
- Клик по популярному городу — то же, что поиск

### 5.2 Боковое меню (`menu_panel.py`)

**Открытие:** клик по кнопке ☰ в хедере → анимированное выдвижение панели слева (ширина 280px)

**Элементы:**
- Заголовок «Menu» (белый) + подзаголовок «Manage your weather preferences» — на фиолетово-синем градиентном фоне
- Кнопка **Saved Cities** (синяя иконка 📍) → переход на `saved_cities_view.py`
- Кнопка **Settings** (розово-фиолетовая иконка ⚙️) → открывает `settings_view.py`
- Секция **Language** — три кнопки EN / RU / KG; активная — выделена синим фоном с ✓

**Логика переключения языка:**
- Сохраняет выбор в `app_settings` (поле `language`)
- Вызывает `language.py → switch_language(code)` → перезагружает все текстовые строки интерфейса без перезапуска приложения

### 5.3 Экран «Saved Cities» (`saved_cities_view.py`)

**Заголовок:** «Saved Cities» (синий) + «Your favorite locations at a glance» (серый)

**Содержимое:**
- Сетка карточек сохранённых городов (по 3 в строке)
- Каждая карточка (`city_card.py`):
  - Тёмно-синий/фиолетовый фон
  - Название города (жирный белый) + дата сохранения
  - Большая температура + описание условия
  - Три мини-плитки: Feels Like, Humidity, Wind
  - Кнопка 🗑️ (удалить) в правом верхнем углу
- Если нет городов → пустое состояние с текстом «No Saved Cities Yet»

**Поведение:**
- Данные берутся из `saved_cities` + актуальный прогноз из `weekly_forecast` (или запрос к API)
- Клик по карточке → переход на главный экран с выбранным городом
- Кнопка «сохранить город» также доступна с главного экрана (иконка ❤️ или +)

### 5.4 Экран «Settings» (`settings_view.py`)

**Секции:**

1. **Display**
   - Единица температуры: переключатель °C / °F (CustomTkinter CTkSwitch)

2. **Notifications**
   - Weather Alerts: переключатель вкл/выкл

3. **Location**
   - Auto-detect Location: переключатель вкл/выкл

**Поведение:**
- Все настройки читаются из / записываются в таблицу `app_settings`
- Изменение единицы температуры → немедленный перерасчёт всех отображаемых значений

### 5.5 Виджет «Календарь» (`calendar_view.py`)

**Открытие:** клик по блоку даты в правом верхнем углу хедера → всплывает попап

**Элементы:**
- Заголовок с текущим месяцем и стрелками ◀ ▶
- Сетка дней (7 × 6)
- Текущий день — выделен красным кружком
- Дни с событиями — точка под числом
- Клик по дню → нижняя панель со списком событий + кнопка «+ Add Event»
- Форма добавления события: поле «Title», поле «Note», кнопка «Save»
- События сохраняются в `calendar_events`

---

## 6. API ПОДКЛЮЧЕНИЕ (OpenWeatherMap)

**Базовый URL:** `https://api.openweathermap.org/data/2.5/`

### Используемые эндпоинты:

| Эндпоинт | Назначение |
|---|---|
| `/weather?q={city}&appid={key}&units=metric` | Текущая погода |
| `/forecast?q={city}&appid={key}&units=metric&cnt=40` | Прогноз на 5 дней / каждые 3 ч → агрегируется до 7 дней |
| `/weather?lat={lat}&lon={lon}&appid={key}` | Погода по координатам (auto-detect) |

**Логика кэширования:**
- Данные считаются свежими в течение **30 минут**
- Проверка: `cached_at` в таблице < 30 мин назад → брать из БД, иначе → запрос к API

**Иконки погоды (SVG-рендер):**
Иконки не загружаются с сервера OWM. Они рисуются кодом через CTkCanvas или PIL на основе `icon_code`:
- `01d` / `01n` → ☀️ (солнце)
- `02d` / `02d` → ⛅ (малооблачно)
- `03x`, `04x` → ☁️ (облачно)
- `09x`, `10x` → 🌧️ (дождь)
- `11x` → ⛈️ (гроза)
- `13x` → ❄️ (снег)
- `50x` → 🌫️ (туман)

---

## 7. МУЛЬТИЯЗЫЧНОСТЬ

**Файлы:** `i18n/en.json`, `i18n/ru.json`, `i18n/kg.json`

**Пример структуры `en.json`:**
```json
{
  "app_title": "Weather Forecast",
  "app_subtitle": "Your personal weather companion for accurate forecasts worldwide",
  "search_placeholder": "Search for a city or location...",
  "search_btn": "Search",
  "popular": "Popular:",
  "feels_like": "Feels like",
  "humidity": "Humidity",
  "wind_speed": "Wind Speed",
  "visibility": "Visibility",
  "pressure": "Pressure",
  "dew_point": "Dew Point",
  "uv_index": "UV Index",
  "today_temp": "Today's Temperature",
  "week_forecast": "7-Day Forecast",
  "menu_title": "Menu",
  "menu_subtitle": "Manage your weather preferences",
  "saved_cities": "Saved Cities",
  "settings": "Settings",
  "language": "Language",
  "display": "Display",
  "temp_unit": "Temperature Unit",
  "notifications": "Notifications",
  "weather_alerts": "Weather Alerts",
  "location": "Location",
  "auto_location": "Auto-detect Location",
  "no_cities": "No Saved Cities Yet",
  "no_cities_sub": "Search for a city and save it to see it here",
  "calendar_title": "Calendar",
  "add_event": "+ Add Event",
  "export_json": "Export as JSON",
  "export_csv": "Export as CSV",
  "export_excel": "Export as Excel",
  "days": {
    "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
    "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday"
  },
  "conditions": {
    "Sunny": "Sunny", "Partly Cloudy": "Partly Cloudy",
    "Cloudy": "Cloudy", "Rainy": "Rainy", "Snowy": "Snowy", "Foggy": "Foggy"
  }
}
```

**Класс `LanguageManager` (`utils/language.py`):**
```python
class LanguageManager:
    def __init__(self):
        self.current = "en"
        self.strings = {}
        self.load("en")

    def load(self, code: str):
        with open(f"i18n/{code}.json", encoding="utf-8") as f:
            self.strings = json.load(f)
        self.current = code

    def t(self, key: str) -> str:
        # Поддержка вложенных ключей: t("days.Monday")
        keys = key.split(".")
        val = self.strings
        for k in keys:
            val = val.get(k, key)
        return val

    def switch(self, code: str, app_instance):
        self.load(code)
        app_instance.refresh_all_texts()  # перерисовать все виджеты
```

---

## 8. ЭКСПОРТ ДАННЫХ

**Компонент:** `export_dialog.py` + `utils/exporter.py`

**Кнопка экспорта:** в секции «7-Day Forecast» → кнопка «Export ▾» → выпадающий список

### 8.1 Форматы экспорта

| Формат | Библиотека | Поля |
|---|---|---|
| **JSON** | `json` (stdlib) | Все поля из `weekly_forecast` + метаданные |
| **CSV** | `csv` (stdlib) | Плоская таблица: дата, день, условие, min, max, влажность, ветер |
| **Excel (.xlsx)** | `openpyxl` | Лист «Forecast» с заголовками + форматированием; лист «Hourly» |

**Пример JSON-экспорта:**
```json
{
  "city": "Bishkek",
  "exported_at": "2026-05-12T14:30:00",
  "unit": "C",
  "forecast": [
    {
      "date": "2026-05-12",
      "day": "Tuesday",
      "condition": "Partly Cloudy",
      "temp_min": 14,
      "temp_max": 22,
      "humidity": 65,
      "wind_speed": 15,
      "pressure": 1013,
      "uv_index": 6
    }
  ]
}
```

**Диалог сохранения файла:** `tkinter.filedialog.asksaveasfilename` с фильтрами типов файлов.

---

## 9. ФИКСИРОВАННОСТЬ РАЗМЕРОВ ПРИ ПОЛНОЭКРАННОМ РЕЖИМЕ

> Критическое требование: при переходе в полноэкранный режим элементы НЕ растягиваются.

**Реализация:**
- Главный контентный фрейм имеет фиксированную ширину: `max_width = 900px`
- Фрейм центрируется через `place(relx=0.5, rely=0, anchor="n")`
- Все внутренние виджеты используют `width=` и `height=` параметры
- `CTkFrame(master, width=900)` + `pack_propagate(False)` → гарантирует фиксированный размер
- Иконки рисуются через `PIL.Image.resize((W, H), LANCZOS)` с заданными константами

```python
# Пример фиксированного размера
stat_icon = CTkLabel(tile, image=icon_img, width=36, height=36, text="")
stat_icon.place(x=12, y=12)  # НЕ grid с stretch
```

---

## 10. ИКОНКА ПРИЛОЖЕНИЯ

**Источник:** `photo_5429185189155376072_y.jpg` (предоставлен пользователем)

**Конвертация (выполняется один раз при сборке):**
```python
# utils/helpers.py
from PIL import Image

def prepare_icons():
    img = Image.open("assets/source_icon.jpg")
    img = img.resize((256, 256), Image.LANCZOS)
    img.save("assets/icon.ico", format="ICO", sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
    img.save("assets/icon.png")
    # macOS: используется .icns через iconutil (отдельный скрипт)
```

**Установка иконки:**
```python
# main.py
app.iconbitmap("assets/icon.ico")          # Windows
app.iconphoto(True, PhotoImage(file="assets/icon.png"))  # Linux / fallback
```

---

## 11. ЗАВИСИМОСТИ (requirements.txt)

```
customtkinter>=5.2.2
Pillow>=10.0.0
requests>=2.31.0
openpyxl>=3.1.2
```

---

## 12. ПОРЯДОК РЕАЛИЗАЦИИ (для ИИ-агента)

### Этап 1 — Инфраструктура
1. Создать структуру папок
2. Написать `config.py` (цвета, шрифты, размеры)
3. Написать `database/db_manager.py` — инициализация SQLite, создание таблиц
4. Написать CRUD-классы для всех таблиц
5. Написать `utils/language.py` и файлы `i18n/`

### Этап 2 — API и данные
6. Написать `api/weather_api.py` — запросы к OWM
7. Написать `api/parser.py` — нормализация ответов
8. Реализовать кэш-логику (30 мин)

### Этап 3 — Компоненты UI
9. Написать базовые компоненты: `stat_tile.py`, `weather_card.py`, `weekly_row.py`
10. Написать `hourly_chart.py` (Canvas-график)
11. Написать `city_card.py`

### Этап 4 — Экраны
12. Написать `main_view.py`
13. Написать `menu_panel.py`
14. Написать `saved_cities_view.py`
15. Написать `settings_view.py`
16. Написать `calendar_view.py`

### Этап 5 — Функциональность
17. Написать `utils/exporter.py` (JSON / CSV / Excel)
18. Написать `export_dialog.py`
19. Подключить переключение языков в `app.py`

### Этап 6 — Сборка и полировка
20. Написать `main.py` — инициализация окна, иконка, запуск
21. Подготовить иконки (PIL)
22. Тестирование всех экранов
23. Проверка фиксированности размеров в полноэкранном режиме

---

## 13. КРИТИЧЕСКИЕ ПРАВИЛА ДЛЯ ИИ-АГЕНТА

1. **Никогда** не использовать `grid(sticky="nsew")` или `pack(expand=True, fill="both")` для элементов с фиксированным размером
2. Все цвета берутся **только** из словаря `COLORS` в `config.py` — никаких хардкод-hex в view-файлах
3. Все текстовые строки берутся **только** через `lang.t("key")` — никакого хардкода текста в UI
4. API-ключ хранится в `config.py` как константа `OWM_API_KEY = "ВАШ_КЛЮЧ"` (не в коде view)
5. Каждый модуль должен иметь docstring с кратким описанием
6. При ошибке API — показывать пользователю сообщение на текущем языке, не крашиться

---

*Документ подготовлен как ТЗ для автоматического агента разработки. Все решения архитектуры, имена файлов и структура БД обязательны к исполнению.*
