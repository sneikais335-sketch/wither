import customtkinter as ctk
import tkinter.filedialog as fd
from config import COLORS, FONTS
from utils.exporter import Exporter
from database.forecast_db import ForecastDB

class ExportDialog(ctk.CTkToplevel):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app_controller
        self.title("Export Data")
        self.geometry("300x250")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=COLORS["bg_page"])

        self._build_ui()
        self.grab_set()

    def _build_ui(self):
        lbl = ctk.CTkLabel(self, text="Select Export Format", font=FONTS["section_head"], text_color=COLORS["text_primary"])
        lbl.pack(pady=20)

        btn_json = ctk.CTkButton(self, text=self.app.lang.t("export_json"), command=self._export_json)
        btn_json.pack(pady=5)

        btn_csv = ctk.CTkButton(self, text=self.app.lang.t("export_csv"), command=self._export_csv)
        btn_csv.pack(pady=5)

        btn_excel = ctk.CTkButton(self, text=self.app.lang.t("export_excel"), command=self._export_excel)
        btn_excel.pack(pady=5)

    def _get_data(self):
        city = self.app.current_city
        if not city:
            return None, None, None
        weekly = ForecastDB.get_weekly_forecast(city)
        hourly = ForecastDB.get_hourly_forecast(city)
        return city, weekly, hourly

    def _export_json(self):
        city, weekly, _ = self._get_data()
        if not weekly: return
        filepath = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filepath:
            Exporter.export_json(filepath, city, self.app.settings.get('temp_unit', 'C'), weekly)
            self.destroy()

    def _export_csv(self):
        _, weekly, _ = self._get_data()
        if not weekly: return
        filepath = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            Exporter.export_csv(filepath, weekly)
            self.destroy()

    def _export_excel(self):
        _, weekly, hourly = self._get_data()
        if not weekly: return
        filepath = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            Exporter.export_excel(filepath, weekly, hourly)
            self.destroy()
