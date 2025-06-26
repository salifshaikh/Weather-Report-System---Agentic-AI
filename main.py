from orchestrator import WeatherSystemOrchestrator
import sys

def main():
    try:
        weather_system = WeatherSystemOrchestrator('weatherHistory.csv')
        results = weather_system.run_analysis()
        weather_system.generate_report(results)
        
    except FileNotFoundError:
        print("Error: weatherHistory.csv not found. Please make sure the file exists.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()