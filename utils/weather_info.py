import requests
from typing import Dict


class WeatherInfo:
    
    def __init__(self,api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"
        
    def get_current_weather(self, location:str) -> Dict:
        
        """Get current weather for a given location."""
        url = f"{self.base_url}/current.json"
        params = {
            "key": self.api_key,
            "q": location
        }
        response = requests.get(url,params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to fetch weather data."}
        
            
    def get_forecast(self, location:str,days: int) -> Dict:
        
        """Get the forecast for a given location."""
        url = f"{self.base_url}/forecast.json"
        params = {
            "key": self.api_key,
            "q": location,
            "days": days  # Default to 3 days forecast
        }
        response = requests.get(url,params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to fetch weather data."}