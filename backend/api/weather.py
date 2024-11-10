import os
from dotenv import load_dotenv
import requests

load_dotenv()


WEATHERBIT_API_KEY = os.getenv("WEATHERBIT_API_KEY")

# https://www.weatherbit.io/api/ag-weather-api-forecast
def get_soil_data(lat: float, lon: float):
    try:
        response = requests.post(f"https://api.weatherbit.io/v2.0/forecast/agweather?lat={lat}&lon={lon}&key={WEATHERBIT_API_KEY}")
        response.raise_for_status()  
        return response.json()
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
