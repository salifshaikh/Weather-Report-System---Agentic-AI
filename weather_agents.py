from base_agent import BaseAgent
from datetime import datetime
import pandas as pd

class DateAgent(BaseAgent):
    def __init__(self):
        super().__init__("DateAgent")
        
    def execute(self):
        today = datetime.now()
        self.log_action(f"Today's date is: {today.strftime('%Y-%m-%d')}")
        return today

class DataLoaderAgent(BaseAgent):
    
    def __init__(self, data_path):
        super().__init__("DataLoaderAgent")
        self.data_path = data_path
        self.data = None
        
    def execute(self):
        self.log_action(f"Loading data from {self.data_path}")
        self.data = pd.read_csv(self.data_path)
        self.data['Formatted Date'] = pd.to_datetime(self.data['Formatted Date'])
        self.log_action(f"Data loaded successfully. Total records: {len(self.data)}")
        return self.data
    
    def get_today_data(self, today_date):
        self.log_action("Fetching the most recent weather data available")
        latest_data = self.data.iloc[-1:]
        return latest_data

class TemperatureAgent(BaseAgent):
    def __init__(self):
        super().__init__("TemperatureAgent")
        
    def execute(self, weather_data):
        if not weather_data.empty:
            temp = weather_data['Temperature (C)'].values[0]
            apparent_temp = weather_data['Apparent Temperature (C)'].values[0]
            
            self.log_action(f"Actual temperature: {temp:.2f}°C")
            self.log_action(f"Feels like: {apparent_temp:.2f}°C")
            
            if temp < 10:
                self.log_action("It's cold! Wear warm clothes.")
            elif temp > 30:
                self.log_action("It's hot! Stay hydrated.")
            else:
                self.log_action("Pleasant temperature!")
                
            return temp, apparent_temp
        else:
            self.log_action("No temperature data available")
            return None, None

class HumidityAgent(BaseAgent):
    def __init__(self):
        super().__init__("HumidityAgent")
        
    def execute(self, weather_data):
        if not weather_data.empty:
            humidity = weather_data['Humidity'].values[0] * 100
            self.log_action(f"Humidity: {humidity:.1f}%")
            
            if humidity > 70:
                self.log_action("High humidity - might feel muggy")
            elif humidity < 30:
                self.log_action("Low humidity - stay moisturized")
            else:
                self.log_action("Comfortable humidity level")
                
            return humidity
        else:
            self.log_action("No humidity data available")
            return None

class WindAgent(BaseAgent):
    def __init__(self):
        super().__init__("WindAgent")
        
    def execute(self, weather_data):
        if not weather_data.empty:
            wind_speed = weather_data['Wind Speed (km/h)'].values[0]
            wind_bearing = weather_data['Wind Bearing (degrees)'].values[0]
            
            self.log_action(f"Wind speed: {wind_speed:.2f} km/h")
            self.log_action(f"Wind direction: {self._get_wind_direction(wind_bearing)} ({wind_bearing}°)")
            
            if wind_speed < 1:
                self.log_action("Calm winds")
            elif wind_speed < 12:
                self.log_action("Light breeze")
            elif wind_speed < 29:
                self.log_action("Moderate breeze")
            else:
                self.log_action("Strong winds - be careful!")
                
            return wind_speed, wind_bearing
        else:
            self.log_action("No wind data available")
            return None, None
    
    def _get_wind_direction(self, degrees):
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]

class WeatherSummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__("WeatherSummaryAgent")
        
    def execute(self, weather_data):
        if not weather_data.empty:
            summary = weather_data['Summary'].values[0]
            precip_type = weather_data['Precip Type'].values[0]
            
            self.log_action(f"Weather summary: {summary}")
            if pd.notna(precip_type):
                self.log_action(f"Precipitation type: {precip_type}")
                
            return summary, precip_type
        else:
            self.log_action("No weather summary available")
            return None, None

class VisibilityPressureAgent(BaseAgent):
    def __init__(self):
        super().__init__("VisibilityPressureAgent")
        
    def execute(self, weather_data):
        if not weather_data.empty:
            visibility = weather_data['Visibility (km)'].values[0]
            pressure = weather_data['Pressure (millibars)'].values[0]
            
            self.log_action(f"Visibility: {visibility:.1f} km")
            self.log_action(f"Pressure: {pressure:.1f} millibars")
            
            if visibility < 1:
                self.log_action("Poor visibility - be careful while driving")
            elif visibility < 5:
                self.log_action("Reduced visibility")
            else:
                self.log_action("Good visibility")
                
            if pressure < 1000:
                self.log_action("Low pressure - possible stormy weather")
            elif pressure > 1020:
                self.log_action("High pressure - generally fair weather")
                
            return visibility, pressure
        else:
            self.log_action("No visibility/pressure data available")
            return None, None
        

class DataAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataAnalysisAgent")
        
    def execute(self, full_data):
        if not full_data.empty:
            self.log_action("Performing statistical analysis...")
            
            avg_temp = full_data['Temperature (C)'].mean()
            max_temp = full_data['Temperature (C)'].max()
            min_temp = full_data['Temperature (C)'].min()
            
            avg_humidity = full_data['Humidity'].mean() * 100
            
            most_common_weather = full_data['Summary'].mode().values[0] if len(full_data['Summary'].mode()) > 0 else "Unknown"
            
            self.log_action(f"Dataset spans from {full_data['Formatted Date'].min()} to {full_data['Formatted Date'].max()}")
            self.log_action(f"Average temperature: {avg_temp:.2f}°C")
            self.log_action(f"Temperature range: {min_temp:.2f}°C to {max_temp:.2f}°C")
            self.log_action(f"Average humidity: {avg_humidity:.1f}%")
            self.log_action(f"Most common weather: {most_common_weather}")
            
            return {
                'avg_temp': avg_temp,
                'temp_range': (min_temp, max_temp),
                'avg_humidity': avg_humidity,
                'common_weather': most_common_weather
            }