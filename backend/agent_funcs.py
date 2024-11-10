from dotenv import load_dotenv
import json
from api.ai import talk_to_chatbot
from instructions import DROUGHT_RISK_PERCENTAGE_PROMPT, LAND_DEGRADATION_RISK_PERCENTAGE_PROMPT, DROUGHT_RISK_PERCENTAGE_PROMPT,CHATBOT_INSTRUCTIONS, RISK_SUMMARY_PROMPT
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
def chatbot_query(query, location, summary, soil_data, population, poverty, land_percentage, drought_percentage):

    context = f"""Here is the information about the location:
    \nLocation: {location}\n
    Land Data: {soil_data}\n
    Summary: {summary}\n
    Population: {population}\n
    Poverty: {poverty}\n"
    Land Degradation Risk throughout the week: {land_percentage}\n
    Drought Risk throughout the week: {drought_percentage}\n
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
