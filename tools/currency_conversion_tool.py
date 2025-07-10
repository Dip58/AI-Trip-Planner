import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from utils.currency_converter import CurrencyConversion

class CurrencyConversionTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for currency conversion.")
        self.currency_service = CurrencyConversion(self.api_key)
        self.currency_converter_tool_list = self.__setup__tools()
        
    def __setup__tools(self):
        """Setup the currency conversion tools."""
        
        @tool
        def currency_converter(self, from_currency: str, to_currency: str,ammount: float = 1.0):
            """Convert currency from one to another.
            Args:
                from_currency (str): The currency to convert from.
                to_currency (str): The currency to convert to.
                ammount (float): The amount to convert. Default is 1.0.
            Important:
                The currency names should be in uppercase (e.g., USD, EUR, GBP,AMD, AED, BDT, AFN)."""
            response= self.currency_service.currency_rate(from_currency, to_currency)
            rate = response.get("conversion_rates", {}).get(to_currency, None)
            return ammount * rate if rate else "Invalid currency or conversion rate not available."
        return [currency_converter]