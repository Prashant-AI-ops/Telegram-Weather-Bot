import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("config/.env")

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data for a given city.
        Returns None if city not found or API error occurs.
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Use metric units by default
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def format_weather_message(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a readable message."""
        try:
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            description = weather_data["weather"][0]["description"]
            city_name = weather_data["name"]
            country = weather_data["sys"]["country"]

            # Get current date and time
            current_time = datetime.now()
            date_str = current_time.strftime("%A, %d %B %Y")
            time_str = current_time.strftime("%I:%M %p")  # 12-hour format with AM/PM

            return (
                f"🌍 Weather in {city_name}, {country}\n"
                f"📅 {date_str}\n"
                f"🕐 {time_str}\n\n"
                f"🌡 Temperature: {temp:.1f}°C\n"
                f"🤔 Feels like: {feels_like:.1f}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind speed: {wind_speed} m/s\n"
                f"☁️ Conditions: {description.capitalize()}"
            )
        except KeyError as e:
            print(f"Error formatting weather data: {e}")
            return "Sorry, couldn't format weather data." 