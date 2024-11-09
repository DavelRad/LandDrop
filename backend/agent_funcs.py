from dotenv import load_dotenv
import json


load_dotenv()

def risk_summary(data):
    """
    Function to return the risk summary based on the data.
    """
    # The risk summary is a simple string for now.
    return "Risk summary for the query: " + data