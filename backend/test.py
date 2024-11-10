from api import weather, ai, location
from agent_funcs import drought_risk
from dotenv import load_dotenv
import json

load_dotenv() 

#print(weather.get_soil_data(34.035, -117.846191), '\n\n')
# print(weather.get_soil_data(34.035, -117.846191), '\n\n')


messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "Hi how are you"
            }
        ]
    }
]

# print(ai.talk_to_chatbot(messages))

# print(location.get_address_from_coords(34.035, -117.846191))
# print(location.get_population_from_coords(34.035, -117.846191))


def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print(drought_risk(data))

load_json_from_file('state.json')