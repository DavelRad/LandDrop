import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

# Configuration
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_KEY_2 = os.getenv("AZURE_OPENAI_API_KEY_2")
GPT_4O_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
GPT_4O_ENDPOINT_2 = os.getenv("AZURE_OPENAI_API_ENDPOINT_2")

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

headers2 = {
    "Content-Type": "application/json",
    "api-key": API_KEY_2,
}


# example messages array
# "messages": [
#       {
#         "role": "system",
#         "content": [
#           {
#             "type": "text",
#             "text": "You are an AI assistant that helps people find information."
#           }
#         ]
#       }
#     ],

def talk_to_chatbot(messages: list):

  payload = {
    "messages": messages,
    "temperature": 0.5,
    "top_p": 0.95,
    "max_tokens": 800
  }

  # request
  try:
      response = requests.post(GPT_4O_ENDPOINT, headers=headers, json=payload)
      response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
      return response.json()['choices'][0]['message']['content']
  except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}")
  
def talk_to_chatbot_2(messages: list):

  payload = {
    "messages": messages,
    "temperature": 0.5,
    "top_p": 0.95,
    "max_tokens": 800
  }

  # request
  try:
      print(f"THIS IS HEADERS 2: {headers2}")
      response = requests.post(GPT_4O_ENDPOINT_2, headers=headers2, json=payload)
      response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
      return response.json()['choices'][0]['message']['content']
  except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}") 