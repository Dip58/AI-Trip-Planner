import os 
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from langchain.tools import tool
from utils.weather_info import WeatherInfo



class WeatherInfoTool:
    """Tool for fetching weather information using OpenWeatherMap API."""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHERMAP_API_KEY is not set in the environment variables.")
        self.weather_service = WeatherInfo(self.api_key)
        self.weather_tool_list = self.__setup__tools()
        
        
    def __setup__tools(self):
        """Setup the weather information tool."""
        
        @tool
        def current_weather(location: str):
            """Get current weather for a given location."""
            
            weather_data = self.weather_service.get_current_weather(location)
            if weather_data:
                loaction = weather_data.get("location", {}).get("name", "Unknown location")
                temp = weather_data.get("current", {}).get("temp_c", "Unknown temperature")
                temp_feel = weather_data.get("current", {}).get("feelslike_c", "Unknown temperature")
                comment = weather_data.get("current", {}).get("condition", {}).get("text", "No comment available")
                wind_speed = weather_data.get("current", {}).get("wind_kph", "Unknown wind speed")
                humadity = weather_data.get("current", {}).get("humidity", "Unknown humidity")
                
                return f"Current weather in {loaction}:\n- Temperature: {temp}°C\n- Feels like: {temp_feel}°C\n- Condition: {comment}\n- Wind Speed: {wind_speed} kph\n- Humidity: {humadity}%"
            else:
                return f"Unable to fetch current weather data."
            
        @tool
        def weather_forecast(location: str, days:int= 3):
            """Get the weather forecast for a given location and number of days from today"""
            
            forecast_data = self.weather_service.get_forecast(location,days)
            if forecast_data:
                location = forecast_data.get("location", {}).get("name", "Unknown location")
                forecast_days = forecast_data.get("forecast", {}).get("forecastday", [])
                
                if not forecast_days:
                    return f"No forecast data available for {location}."
                
                forecast_str = f"Weather forecast for {location}:\n"
                
                for day in forecast_days:
                    date = day.get("date", "Unknown date")
                    
                    if date == "Unknown date":
                        continue  # Skip if date is not available
                    
                    condition = day.get("day", {}).get("condition", {}).get("text", "No condition available")
                    max_temp = day.get("day", {}).get("maxtemp_c", "Unknown max temperature")
                    min_temp = day.get("day", {}).get("mintemp_c", "Unknown min temperature")
                    avg_temp = day.get("day", {}).get("avgtemp_c", "Unknown average temperature")
                    max_wind = day.get("day", {}).get("maxwind_kph", "Unknown max wind speed")
                    chance_of_rain = day.get("day", {}).get("daily_chance_of_rain", "Unknown chance of rain")
                    humidity = day.get("day", {}).get("avghumidity", "Unknown humidity")
                    
                    forecast_str += f"""
                                    -------------------------------------------
                                    Date: {date}
                                    - Condition: {condition}
                                    - Max Temperature: {max_temp}°C
                                    - Min Temperature: {min_temp}°C
                                    - Average Temperature: {avg_temp}°C
                                    - Max Wind Speed: {max_wind} kph
                                    - Chance of Rain: {chance_of_rain}%
                                    - Humidity: {humidity}%
                                    -------------------------------------------
                                    """
                    
                return forecast_str
            else:
                return f"Unable to fetch weather forecast data."
            
        return [current_weather, weather_forecast]
                
                
            
            