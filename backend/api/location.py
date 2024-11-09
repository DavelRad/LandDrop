import requests
import os

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_address_from_coords(lat: float, lon: float):
    try:
        response = requests.get(f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey={GEOAPIFY_API_KEY}")
        response.raise_for_status()  
        responseJSON = response.json()
        return f"{responseJSON["features"][0]["properties"]["city"]}, {responseJSON["features"][0]["properties"]["state"]}, {responseJSON["features"][0]["properties"]["country"]}"
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")