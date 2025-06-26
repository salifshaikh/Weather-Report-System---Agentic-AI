from weather_agents import *

class WeatherSystemOrchestrator:
    def __init__(self, data_path):
        self.agents = {
            'date': DateAgent(),
            'data_loader': DataLoaderAgent(data_path),
            'temperature': TemperatureAgent(),
            'humidity': HumidityAgent(),
            'wind': WindAgent(),
            'summary': WeatherSummaryAgent(),
            'visibility_pressure': VisibilityPressureAgent()
        }
        
    def run_analysis(self):
        print("WEATHER AGENT SYSTEM")
        
        today = self.agents['date'].execute()
        
        weather_data = self.agents['data_loader'].execute()
        
        latest_data = self.agents['data_loader'].get_today_data(today)
        
        if not latest_data.empty:
            data_date = latest_data['Formatted Date'].values[0]
            print(f"\n📅 Analyzing weather data from: {pd.to_datetime(data_date).strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        temp, apparent_temp = self.agents['temperature'].execute(latest_data)
        humidity = self.agents['humidity'].execute(latest_data)
        wind_speed, wind_bearing = self.agents['wind'].execute(latest_data)
        summary, precip = self.agents['summary'].execute(latest_data)
        visibility, pressure = self.agents['visibility_pressure'].execute(latest_data)
        
        results = {
            'date': today,
            'data_date': pd.to_datetime(data_date) if not latest_data.empty else None,
            'temperature': temp,
            'apparent_temperature': apparent_temp,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'wind_bearing': wind_bearing,
            'summary': summary,
            'precipitation': precip,
            'visibility': visibility,
            'pressure': pressure
        }
        
        return results
    
    def generate_report(self, results):
        print("COMPREHENSIVE WEATHER REPORT")
        
        if results['temperature'] is not None:
            print(f"\n📊 Weather Conditions:")
            print(f"Summary: {results['summary']}")
            print(f"Temperature: {results['temperature']:.1f}°C (Feels like: {results['apparent_temperature']:.1f}°C)")
            print(f"Humidity: {results['humidity']:.1f}%")
            print(f"Wind: {results['wind_speed']:.1f} km/h")
            print(f"Visibility: {results['visibility']:.1f} km")
            print(f"Pressure: {results['pressure']:.1f} mb")
            
            if results['precipitation']:
                print(f"   Precipitation: {results['precipitation']}")
            
            print("\nRecommendations:")
            
            if results['temperature'] < 0:
                print("Freezing conditions - dress very warmly!")
            elif results['temperature'] < 10:
                print("Cold weather - wear a jacket")
            elif results['temperature'] > 30:
                print("Hot weather - use sunscreen and stay hydrated")
            
            if results['precipitation'] == 'rain':
                print("Don't forget your umbrella!")
            elif results['precipitation'] == 'snow':
                print("Snow expected - drive carefully!")
            
            if results['wind_speed'] > 25:
                print("Strong winds - secure loose objects")
                
            if results['visibility'] < 5:
                print("Reduced visibility - drive with caution")
                
        else:
            print("Insufficient data for complete report")