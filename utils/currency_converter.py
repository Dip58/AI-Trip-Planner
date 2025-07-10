import requests
from langchain_core.tools import tool

class CurrencyConversion:
    
    def __init__(self, api_key: str):
        """Initialize the CurrencyConversion with an API key."""
        if not api_key:
            raise ValueError("API key is required for currency conversion.")
        self.api_key = api_key
        self.base_url = "https://api.freecurrencyapi.com/"
        
    def currency_rate(self, from_currency: str, to_currency: str):
        """Gives the conversion rate from one currency to another. 
        Args:
            from_currency (str): The currency to convert from.
            to_currency (str): The currency to convert to."""
            
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to fetch currency data. The requested currency name might be wrong"}