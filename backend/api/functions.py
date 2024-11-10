import os
from dotenv import load_dotenv
import requests

load_dotenv()

WEATHERBIT_API_KEY = os.getenv("WEATHERBIT_API_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_address_from_coords(lat: float, lon: float):
    try:
        response = requests.get(f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey={GEOAPIFY_API_KEY}")
        response.raise_for_status()  
        responseJSON = response.json()
        return f"{responseJSON['features'][0]['properties']['city']}, {responseJSON['features'][0]['properties']['state']}, {responseJSON['features'][0]['properties']['country']}"
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

# https://www.weatherbit.io/api/ag-weather-api-forecast
def get_soil_data(lat: float, lon: float):
    try:
        response = requests.post(f"https://api.weatherbit.io/v2.0/forecast/agweather?lat={lat}&lon={lon}&key={WEATHERBIT_API_KEY}")
        response.raise_for_status()  
        return response.json()
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

def get_place_code_from_coords(lat: float, lon: float):
    try:
        response = requests.get(
            f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={lon}&y={lat}&benchmark=Public_AR_Current&vintage=Current_Current&format=json"
        )
        response.raise_for_status()
        data = response.json()
        
        # Check for "Incorporated Places" key as a fallback for "Places"
        if "Incorporated Places" in data["result"]["geographies"] and data["result"]["geographies"]["Incorporated Places"]:
            state_code = data["result"]["geographies"]["States"][0]["STATE"]
            place_code = data["result"]["geographies"]["Incorporated Places"][0]["PLACE"]
            return state_code, place_code
        
        # Fallback to County if neither Place nor Incorporated Place data is found
        elif "Counties" in data["result"]["geographies"] and data["result"]["geographies"]["Counties"]:
            state_code = data["result"]["geographies"]["States"][0]["STATE"]
            county_code = data["result"]["geographies"]["Counties"][0]["COUNTY"]
            print(f"Place code not found; using county code {county_code} instead.")
            return state_code, county_code
        
        # Raise an error if no appropriate location data is found
        else:
            raise ValueError("Place or County not found for the given coordinates.")
        
    except Exception as e:
        raise SystemExit(f"Failed to get place code from coordinates. Error: {e}")

def get_population_data(lat: float, lon: float):
    try:
        # Get state and place codes from coordinates
        state_code, place_code = get_place_code_from_coords(lat, lon)
        
        # Query Census API for population data
        response = requests.get(
            f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B01003_001E&for=place:{place_code}&in=state:{state_code}"
        )
        response.raise_for_status()
        data = response.json()
        
        # Return only the population number
        return int(data[1][1])
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    

def get_poverty_data(lat: float, lon: float):
    try:
        # Get state and place codes from coordinates
        state_code, place_code = get_place_code_from_coords(lat, lon)
        
        # Query Census API for poverty data
        response = requests.get(
            f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B17001_002E&for=place:{place_code}&in=state:{state_code}"
        )
        response.raise_for_status()
        data = response.json()
        
        # Return only the poverty number
        return int(data[1][1])
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
