from dotenv import load_dotenv
import json
from api.ai import talk_to_chatbot
import re
from instructions import RISK_SUMMARY_PROMPT, RISK_PERCENTAGE_PROMPT, DROUGHT_RISK_INSTRUCTIONS


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

def risk_percentage(data, summary):
    print('in here')
    messages = [
    {
        "role": "system",
        "content": f"Here is your prompt: {RISK_PERCENTAGE_PROMPT}. Remember to only respond with a single number between 10 and 90."
    },
    {
        "role": "user",
        "content": f"This is the data reference: {data}\n This is the summary: {summary}"
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
            "content": f"{DROUGHT_RISK_INSTRUCTIONS}"
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