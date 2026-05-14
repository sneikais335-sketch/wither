import json
import csv
import datetime
from openpyxl import Workbook

class Exporter:
    @staticmethod
    def export_json(filepath, city_name, unit, forecast_data):
        data = {
            "city": city_name,
            "exported_at": datetime.datetime.now().isoformat(),
            "unit": unit,
            "forecast": forecast_data
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def export_csv(filepath, forecast_data):
        if not forecast_data:
            return
            
        keys = forecast_data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(forecast_data)

    @staticmethod
    def export_excel(filepath, forecast_data, hourly_data=None):
        wb = Workbook()
        
        # Weekly sheet
        ws_week = wb.active
        ws_week.title = "7-Day Forecast"
        if forecast_data:
            keys = list(forecast_data[0].keys())
            ws_week.append(keys)
            for row in forecast_data:
                ws_week.append([row[k] for k in keys])
                
        # Hourly sheet
        if hourly_data:
            ws_hour = wb.create_sheet(title="Hourly Forecast")
            keys = list(hourly_data[0].keys())
            ws_hour.append(keys)
            for row in hourly_data:
                ws_hour.append([row[k] for k in keys])

        wb.save(filepath)
