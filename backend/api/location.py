import requests
import os
from .ai import talk_to_chatbot

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_address_from_coords(lat: float, lon: float):
    try:
        response = requests.get(f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey={GEOAPIFY_API_KEY}")
        response.raise_for_status()  
        responseJSON = response.json()
        return f"{responseJSON["features"][0]["properties"]["city"]}, {responseJSON["features"][0]["properties"]["state"]}, {responseJSON["features"][0]["properties"]["country"]}"
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
def get_population_from_coords(lat: float, lon: float):
    try:
        address = get_address_from_coords(lat, lon)

        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps the user find the population based off a city, state, and country. The user will input the city, state, and country. Only send back the population as a number and nothing else."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{address}"
                    }
                ]
            }
        ]
        
        return talk_to_chatbot(messages)
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")