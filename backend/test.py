from api import weather
from api import ai
from dotenv import load_dotenv

load_dotenv() 

print(weather.get_soil_data(34.035, -117.846191), '\n\n')


messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    }
]

print(ai.talk_to_chatbot(messages))
