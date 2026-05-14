import customtkinter as ctk
import datetime
import calendar
from config import COLORS, FONTS
from database.calendar_db import CalendarDB

class CalendarView(ctk.CTkToplevel):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app_controller
        self.title(self.app.lang.t("calendar_title"))
        self.geometry("400x500")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=COLORS["bg_page"])

        self.current_date = datetime.date.today()
        self.selected_date = self.current_date

        self._build_ui()
        self.update_calendar()

    def _build_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", pady=10)

        self.btn_prev = ctk.CTkButton(self.header, text="◀", width=30, command=self._prev_month, fg_color="transparent", text_color=COLORS["text_primary"])
        self.btn_prev.pack(side="left", padx=10)

        self.lbl_month = ctk.CTkLabel(self.header, text="", font=FONTS["section_head"], text_color=COLORS["text_primary"])
        self.lbl_month.pack(side="left", expand=True)

        self.btn_next = ctk.CTkButton(self.header, text="▶", width=30, command=self._next_month, fg_color="transparent", text_color=COLORS["text_primary"])
        self.btn_next.pack(side="right", padx=10)

        # Days of week
        days_frame = ctk.CTkFrame(self, fg_color="transparent")
        days_frame.pack(fill="x", padx=10)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            lbl = ctk.CTkLabel(days_frame, text=d, font=("Segoe UI", 10, "bold"), text_color=COLORS["text_secondary"], width=45)
            lbl.grid(row=0, column=i, padx=2)

        # Calendar grid
        self.grid_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=10)
        self.grid_frame.pack(fill="x", padx=10, pady=10)

        # Events list below
        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=100)
        self.events_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.btn_add = ctk.CTkButton(
            self, text=self.app.lang.t("add_event"), 
            font=FONTS["btn_text"], fg_color=COLORS["accent_blue"],
            command=self._add_event_dialog
        )
        self.btn_add.pack(pady=10)

    def update_calendar(self):
        self.lbl_month.configure(text=self.current_date.strftime("%B %Y"))
        
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Fetch events for this month to show dots
        # Simplified: fetch all events
        all_events = CalendarDB.get_events()
        event_dates = {e['date'] for e in all_events}

        today = datetime.date.today()

        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                if day == 0:
                    continue
                
                day_date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                
                btn_color = "transparent"
                text_color = COLORS["text_primary"]
                
                if day == today.day and self.current_date.month == today.month and self.current_date.year == today.year:
                    btn_color = "#EF4444" # Red for today
                    text_color = "white"
                elif day_date_str == self.selected_date.strftime("%Y-%m-%d"):
                    btn_color = COLORS["menu_item_hover"]

                btn = ctk.CTkButton(
                    self.grid_frame, text=str(day), width=45, height=35,
                    fg_color=btn_color, text_color=text_color, hover_color=COLORS["menu_item_hover"],
                    command=lambda d=day: self._select_date(d)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)

                if day_date_str in event_dates:
                    # Draw a tiny dot (using a label)
                    dot = ctk.CTkLabel(btn, text="•", text_color=COLORS["accent_purple"], font=("Segoe UI", 16))
                    dot.place(relx=0.5, rely=0.8, anchor="center")

        self._load_events_for_selected()

    def _select_date(self, day):
        self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
        self.update_calendar()

    def _prev_month(self):
        # Subtract a month
        first = self.current_date.replace(day=1)
        prev_month = first - datetime.timedelta(days=1)
        self.current_date = prev_month.replace(day=1)
        self.update_calendar()

    def _next_month(self):
        # Add a month
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        last = self.current_date.replace(day=days_in_month)
        next_month = last + datetime.timedelta(days=1)
        self.current_date = next_month.replace(day=1)
        self.update_calendar()

    def _load_events_for_selected(self):
        for w in self.events_frame.winfo_children():
            w.destroy()
            
        date_str = self.selected_date.strftime("%Y-%m-%d")
        events = CalendarDB.get_events(date_str)
        
        if not events:
            lbl = ctk.CTkLabel(self.events_frame, text="No events", text_color=COLORS["text_secondary"])
            lbl.pack(pady=10)
            return

        for e in events:
            f = ctk.CTkFrame(self.events_frame, fg_color=COLORS["bg_card"], corner_radius=5)
            f.pack(fill="x", pady=2)
            lbl = ctk.CTkLabel(f, text=e['title'], text_color=COLORS["text_primary"])
            lbl.pack(side="left", padx=10, pady=5)
            btn_del = ctk.CTkButton(f, text="✕", width=20, fg_color="transparent", text_color="#EF4444", command=lambda id=e['id']: self._del_event(id))
            btn_del.pack(side="right", padx=5)

    def _add_event_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter event title:", title="Add Event")
        # In CustomTkinter, dialog blocks but must be shown. Actually CTkInputDialog handles its own window.
        title = dialog.get_input()
        if title:
            CalendarDB.add_event(self.selected_date.strftime("%Y-%m-%d"), title)
            self.update_calendar()

    def _del_event(self, event_id):
        CalendarDB.delete_event(event_id)
        self.update_calendar()
