 
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import UserRequest, Response
from agent_funcs import risk_summary, risk_percentage
from api.weather import get_soil_data
from uagents.setup import fund_agent_if_low
import json
from agent_funcs import chatbot_query

load_dotenv()

# Initialize the agent with its configuration.
chatbot_agent = Agent(
    name="Chatbot Agent",
    seed="Chatbot Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)
fund_agent_if_low(chatbot_agent.wallet.address())

def load_json_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

 
@chatbot_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {chatbot_agent.name}")
    ctx.logger.info(f"With address: {chatbot_agent.address}")
    ctx.logger.info(f"And wallet address: {chatbot_agent.wallet.address()}")
 
# Decorator to handle incoming queries.
@chatbot_agent.on_query(model=UserRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: UserRequest):
    user_address = sender
    query = _query.query
    try:
        # Load data from JSON file
        data = load_json_data()
        location_data = None

        # Find matching data based on location if provided
        for entry in data.get("location_data", []):
            if entry.get("location") == _query.query:  # Assuming the query contains the location name
                location_data = entry
                break

        if location_data:
            land_data = location_data.get("land_data")
            summary = location_data.get("summary")
            risk_percentage = location_data.get("risk_percentage")
            location = location_data.get("location")
            city = location_data.get("city")

        response = chatbot_query(query, land_data, summary, risk_percentage, location, city)
        if response:
            await ctx.send(
                sender,
                Response(
                    text="success",
                )
            )
        else:
            # If no data is found, send a fail response
            await ctx.send(sender, Response(text="Location not found in data."))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

# Main execution block to run the agent.
if __name__ == "__main__":
    chatbot_agent.run()
    