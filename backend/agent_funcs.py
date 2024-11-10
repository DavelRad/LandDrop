from dotenv import load_dotenv
import json
from api.ai import talk_to_chatbot
from instructions import RISK_SUMMARY_PROMPT, LAND_DEGRADATION_RISK_PERCENTAGE_PROMPT, DROUGHT_RISK_PERCENTAGE_PROMPT,CHATBOT_INSTRUCTIONS

load_dotenv()

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

def location_data_assistant(query, land_data, summary, risk_percentage, location, city):

    context = "Here is the information about various locations:\n"

    context += f"Here is the information about the location \nLocation: {location}\n City: {city}\n Land Data: {land_data}\nSummary: {summary}\nRisk Percentage: {risk_percentage}\n"

    messages = [
        {
            "role": "system",
            "content": {CHATBOT_INSTRUCTIONS}
        },
        {
            "role": "assistant",
            "content": context
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = talk_to_chatbot(messages)
    return response