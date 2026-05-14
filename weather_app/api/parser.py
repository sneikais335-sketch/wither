import datetime

class WeatherParser:
    @staticmethod
    def parse_current(data):
        if not data:
            return None
            
        weather = data.get('weather', [{}])[0]
        main = data.get('main', {})
        wind = data.get('wind', {})
        
        # OWM 2.5/weather doesn't give UV index directly. We'll mock it or omit it unless we call OneCall.
        # But we need it for the UI. We'll just default to 0 if not present.
        # Dew point can be approximated if not given: temp - ((100 - humidity)/5)
        temp = main.get('temp', 0)
        humidity = main.get('humidity', 0)
        dew_point = temp - ((100 - humidity) / 5) if humidity else 0
        
        condition_map = {
            "Clear": "Sunny", "Clouds": "Cloudy", "Rain": "Rainy",
            "Drizzle": "Rainy", "Thunderstorm": "Rainy", "Snow": "Snowy", "Mist": "Foggy",
            "Smoke": "Foggy", "Haze": "Foggy", "Dust": "Foggy", "Fog": "Foggy",
            "Sand": "Foggy", "Ash": "Foggy", "Squall": "Rainy", "Tornado": "Rainy"
        }
        main_condition = weather.get('main', 'Clear')
        mapped_condition = condition_map.get(main_condition, main_condition)
        
        if main_condition == "Clouds" and weather.get('id', 0) in (801, 802):
            mapped_condition = "Partly Cloudy"

        return {
            'name': data.get('name', 'Unknown'),
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'temp': temp,
            'feels_like': main.get('feels_like', temp),
            'condition': mapped_condition,
            'icon_code': weather.get('icon', '01d'),
            'humidity': humidity,
            'wind_speed': wind.get('speed', 0) * 3.6, # m/s to km/h
            'pressure': main.get('pressure', 0),
            'visibility': data.get('visibility', 0) / 1000, # m to km
            'dew_point': round(dew_point, 1),
            'uv_index': 0 # Not provided by default in standard /weather
        }

    @staticmethod
    def parse_weekly(data):
        if not data:
            return []
            
        daily_data = {}
        for item in data.get('list', []):
            dt_txt = item.get('dt_txt', '')
            date_str = dt_txt.split(' ')[0] # YYYY-MM-DD
            
            if date_str not in daily_data:
                daily_data[date_str] = {
                    'date': date_str,
                    'temps': [],
                    'weather': [],
                    'humidities': [],
                    'wind_speeds': [],
                    'pressures': []
                }
                
            daily_data[date_str]['temps'].append(item.get('main', {}).get('temp', 0))
            daily_data[date_str]['weather'].append(item.get('weather', [{}])[0])
            daily_data[date_str]['humidities'].append(item.get('main', {}).get('humidity', 0))
            daily_data[date_str]['wind_speeds'].append(item.get('wind', {}).get('speed', 0))
            daily_data[date_str]['pressures'].append(item.get('main', {}).get('pressure', 0))

        weekly_forecast = []
        for date_str, values in daily_data.items():
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt.strftime("%A")
            
            # Find most common weather condition and icon for the day
            icons = [w.get('icon', '01d') for w in values['weather']]
            main_conds = [w.get('main', 'Clear') for w in values['weather']]
            
            common_icon = max(set(icons), key=icons.count) if icons else '01d'
            common_cond = max(set(main_conds), key=main_conds.count) if main_conds else 'Clear'
            
            condition_map = {
                "Clear": "Sunny", "Clouds": "Cloudy", "Rain": "Rainy",
                "Drizzle": "Rainy", "Thunderstorm": "Rainy", "Snow": "Snowy", "Mist": "Foggy",
                "Smoke": "Foggy", "Haze": "Foggy", "Dust": "Foggy", "Fog": "Foggy",
                "Sand": "Foggy", "Ash": "Foggy", "Squall": "Rainy", "Tornado": "Rainy"
            }
            mapped_condition = condition_map.get(common_cond, common_cond)
            if common_cond == "Clouds" and any(w.get('id', 0) in (801, 802) for w in values['weather']):
                mapped_condition = "Partly Cloudy"

            avg_humidity = sum(values['humidities']) / len(values['humidities']) if values['humidities'] else 0
            
            weekly_forecast.append({
                'date': date_str,
                'day_name': day_name,
                'condition': mapped_condition,
                'icon_code': common_icon,
                'temp_min': min(values['temps']) if values['temps'] else 0,
                'temp_max': max(values['temps']) if values['temps'] else 0,
                'humidity': int(avg_humidity),
                'wind_speed': (sum(values['wind_speeds']) / len(values['wind_speeds'])) * 3.6,
                'pressure': int(sum(values['pressures']) / len(values['pressures'])),
                'visibility': 10, # mock
                'dew_point': 0, # mock
                'uv_index': 0 # mock
            })
            
        return weekly_forecast[:7] # Return up to 7 days (usually 5 from this endpoint)

    @staticmethod
    def parse_hourly(data):
        if not data:
            return []
            
        hourly_forecast = []
        # Return next 8 intervals (24 hours)
        for item in data.get('list', [])[:8]:
            weather = item.get('weather', [{}])[0]
            
            condition_map = {"Clear": "Sunny", "Clouds": "Cloudy", "Rain": "Rainy", "Snow": "Snowy", "Mist": "Foggy"}
            main_cond = weather.get('main', 'Clear')
            mapped_condition = condition_map.get(main_cond, main_cond)
            
            hourly_forecast.append({
                'datetime': item.get('dt_txt'),
                'temp': item.get('main', {}).get('temp', 0),
                'condition': mapped_condition,
                'icon_code': weather.get('icon', '01d')
            })
            
        return hourly_forecast
