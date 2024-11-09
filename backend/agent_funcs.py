from dotenv import load_dotenv
import json
from api.ai import talk_to_chatbot
from instructions import *


load_dotenv()

def risk_summary(data):
    """
    Function to return the risk summary based on the data.
    """
    messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": f"Here is your prompt: {RISK_SUMMARY_PROMPT}"
            }
        ],
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"This is the data you need to analyze: {data}"
            }
        ],
    }
    ]

    response = talk_to_chatbot(messages)
    return response

def risk_percentage(data, summary):
    messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": f"Here is your prompt: {RISK_PERCENTAGE_PROMPT}"
            }
        ],
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"This is the data reference: {data}\n This is the summary: {summary}"
            }
        ],
    }
    ]
    response = talk_to_chatbot(messages)
    return response