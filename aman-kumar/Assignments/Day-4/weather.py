import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

# Load environment variables
API_KEY = os.environ.get("API_KEY")
CITY = input("Enter the city name: ").lower().strip()

if not API_KEY:
    raise ValueError("API_KEY not found. Please set the API_KEY environment variable.")

try:
    # Step 1: Get current weather data for the city (no One Call API)
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(current_weather_url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract relevant information from current weather data
    city_name = data["name"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]
    timestamp = data["dt"]
    utc_dt = datetime.utcfromtimestamp(timestamp)
    ist_dt = utc_dt + timedelta(hours=5, minutes=30)
    date_time_ist = ist_dt.strftime('%Y-%m-%d %H:%M:%S IST')

    # Print the weather information
    print(f"City: {city_name}")
    print(f"Date and Time (IST): {date_time_ist}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather Description: {weather_description}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
