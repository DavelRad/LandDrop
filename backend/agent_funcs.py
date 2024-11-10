from dotenv import load_dotenv
import json
from api.ai import talk_to_chatbot
from instructions import DROUGHT_RISK_PERCENTAGE_PROMPT, LAND_DEGRADATION_RISK_PERCENTAGE_PROMPT, DROUGHT_RISK_PERCENTAGE_PROMPT,CHATBOT_INSTRUCTIONS, RISK_SUMMARY_PROMPT, SOIL_DATA_PREDICTOR_INSTRUCTION, LAND_RISK_PREDICTOR_PROMPT, DROUGHT_RISK_PREDICTOR_PROMPT, PREDICTION_RISK_SUMMARY_PROMPT, MIGRATION_PATTERNS_PROMPT, AREA_TYPE_PROMPT, GRADUATION_RATE_PROMPT
import re

load_dotenv()
def risk_summary(data):
    """
    Function to return the risk summary based on the data.
    """
    messages = [
        {
            "role": "system",
            "content": f"Here is your prompt: {RISK_SUMMARY_PROMPT}"
        },
        {
            "role": "user",
            "content": f"This is the data you need to analyze: {data}"
        }
    ]

    response = talk_to_chatbot(messages)
    return response

def land_degradation_risk_percentage(data):
    print('in here')
    messages = [
    {
        "role": "system",
        "content": f"Here is your prompt: {LAND_DEGRADATION_RISK_PERCENTAGE_PROMPT}. Remember to only respond with a single number between 10 and 90."
    },
    {
        "role": "user",
        "content": f"This is the data reference: {data}"
    }
]
    response = talk_to_chatbot(messages)
    return response

def drought_risk_percentage(data):
    print('in here')
    messages = [
    {
        "role": "system",
        "content": f"Here is your prompt: {DROUGHT_RISK_PERCENTAGE_PROMPT}. Remember to only respond with a single number between 10 and 90."
    },
    {
        "role": "user",
        "content": f"This is the data reference: {data}"
    }
]
    response = talk_to_chatbot(messages)
    return response
def chatbot_query(query, location, summary, soil_data, population, poverty, land_percentage, drought_percentage, chat_history):

    context = f"""Here is the information about the location:
    \nLocation: {location}\n
    Land Data: {soil_data}\n
    Summary: {summary}\n
    Population: {population}\n
    Poverty: {poverty}\n"
    Land Degradation Risk throughout the week: {land_percentage}\n
    Drought Risk throughout the week: {drought_percentage}\n
    Conversation History: {chat_history}\n
    """

    messages = [
        {
            "role": "system",
            "content": CHATBOT_INSTRUCTIONS + context
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = talk_to_chatbot(messages)
    return response

def drought_risk(data):
    """
    Function to return the drought risk based on the data.
    """
    messages = [
        {
            "role": "system",
            "content": f"{DROUGHT_RISK_PERCENTAGE_PROMPT}"
        },
        {
            "role": "user",
            "content": f"{data}"
        }
    ]

    response = talk_to_chatbot(messages)
    cleaned_response = re.sub(r'^```json|```$', '', response.strip())
    json_string = json.loads(cleaned_response)
    return json_string

async def generate_soil_data_predictions(soil_data: list) -> list:
    """
    Generate future predictions for multiple days in one LLM call. The response should be a 
    list of arrays, each containing predicted values for a single day in the specified order.
    """
    messages = [
        {
            "role": "system",
            "content": SOIL_DATA_PREDICTOR_INSTRUCTION
        },
        {
            "role": "user",
            "content": f"Here is the historical soil data: {soil_data}"
        }
    ]
    response = talk_to_chatbot(messages)
    print(f"Raw LLM response: {response}")
    try:
        predicted_values_list = json.loads(response)  # Assuming LLM response is JSON-parsable
        
        # Create the future soil data based on parsed response
        future_soil_data = []
        for day_index, predicted_values in enumerate(predicted_values_list[:9]):
            predicted_day = {
                "bulk_soil_density": predicted_values[0],
                "evapotranspiration": predicted_values[1],
                "precip": predicted_values[2],
                "temp_2m_avg": predicted_values[3],
                "wind_10m_spd_avg": predicted_values[4],
                "v_soilm_0_10cm": predicted_values[5],
                "v_soilm_100_200cm": predicted_values[6],
                "v_soilm_10_40cm": predicted_values[7],
                "v_soilm_40_100cm": predicted_values[8],
                "valid_date": soil_data[day_index]["valid_date"]
            }
            future_soil_data.append(predicted_day)
        
        return future_soil_data

    except json.JSONDecodeError:
        # Handle any parsing issues here, possibly logging them or defaulting values
        print(f"Failed to parse LLM response: {response}")
        return []

def predict_land_percentage(land_percentage: float) -> float:
    """
    Predict future land degradation percentages based on historical data.
    """
    messages = [
        {
            "role": "system",
            "content": f"Here is your prompt: {LAND_RISK_PREDICTOR_PROMPT}"
        },
        {
            "role": "user",
            "content": f"This is the historical land percentage data: {land_percentage}"
        }
    ]

    # Call the chatbot function
    response = talk_to_chatbot(messages)

    # Clean and parse the response
    cleaned_response = re.sub(r'^```json|```$', '', response.strip())
    try:
        predicted_land_percentage = json.loads(cleaned_response)
        return predicted_land_percentage

    except json.JSONDecodeError:
        print(f"Failed to parse LLM response for land percentage: {response}")
        return []

def predict_drought_percentage(drought_percentage: list) -> list:
    """
    Predict future drought percentages based on historical data.
    """
    messages = [
        {
            "role": "system",
            "content": f"Here is your prompt: {DROUGHT_RISK_PREDICTOR_PROMPT}"
        },
        {
            "role": "user",
            "content": f"This is the historical drought percentage data: {drought_percentage}"
        }
    ]

    # Call the chatbot function
    response = talk_to_chatbot(messages)

    # Clean and parse the response
    cleaned_response = re.sub(r'^```json|```$', '', response.strip())
    try:
        predicted_drought_percentage = json.loads(cleaned_response)
        return predicted_drought_percentage

    except json.JSONDecodeError:
        print(f"Failed to parse LLM response for drought percentage: {response}")
        return []
    
async def generate_summary_prediction(summary, soil_data, land_percentage, drought_percentage):
    """
    Generate a summary prediction based on provided environmental data.
    """
    # Combine data into a context for the LLM
    context = f"""
    Current Summary: {summary}
    Soil Data: {soil_data}
    Land Degradation Risk Percentages: {land_percentage}
    Drought Risk Percentages: {drought_percentage}
    """

    # Define messages to send to the LLM
    messages = [
        {
            "role": "system",
            "content": f"Here is your prompt: {PREDICTION_RISK_SUMMARY_PROMPT}"
        },
        {
            "role": "user",
            "content": f"This is the data you need to analyze: {context}"
        }
    ]

    # Call the chatbot function
    response = talk_to_chatbot(messages)

    # Clean the response by removing any extraneous formatting
    cleaned_response = re.sub(r'^```json|```$', '', response.strip())
    
    return cleaned_response

def get_migration_patterns(location):
    """
    Retrieve migration patterns for a specified location.

    Parameters:
    - location (str): The region or location identifier for which to fetch migration data.

    Returns:
    - dict: A dictionary containing the destination regions and their corresponding migration volume percentages.
    """

    messages = [
        {
            "role": "system",
            "content": MIGRATION_PATTERNS_PROMPT
        },
        {
            "role": "user",
            "content": f"The location for migration patterns analysis is: {location}."
        }
    ]

    # Call the chatbot function to get migration patterns
    response = talk_to_chatbot(messages)

    # Clean up and format response if necessary
    cleaned_response = re.sub(r'^```|```$', '', response.strip())
    
    return cleaned_response

def get_area_type(location):
    messages = [
        {
            "role": "system",
            "content": AREA_TYPE_PROMPT
        },
        {
            "role": "user",
            "content": f"The location to classify is {location}."
        }
    ]

    response = talk_to_chatbot(messages)
    return response.strip()


def get_graduation_rate(location):
    """
    Function to retrieve the graduation rate for a specified location.
    """
    # Define messages to send to the LLM
    messages = [
        {
            "role": "system",
            "content": GRADUATION_RATE_PROMPT
        },
        {
            "role": "user",
            "content": f"Please provide the graduation rate for the following location: {location}"
        }
    ]

    # Call the chatbot function
    response = talk_to_chatbot(messages)

    # Clean the response, ensuring it only contains the percentage
    cleaned_response = response.strip()
    return cleaned_response