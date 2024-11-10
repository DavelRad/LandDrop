 
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import UserRequest, Response
from agent_funcs import risk_summary
from api.functions import get_soil_data
from uagents.setup import fund_agent_if_low
import json
from agent_funcs import chatbot_query

load_dotenv()

# Initialize the agent with its configuration.
chatbot_agent = Agent(
    name="Chatbot Agent",
    seed="Chatbot Secret Phrase",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)
fund_agent_if_low(chatbot_agent.wallet.address())

def load_json_data():
    with open("state.json", "r") as file:
        data = json.load(file)
    return data

 
@chatbot_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {chatbot_agent.name}")
    ctx.logger.info(f"With address: {chatbot_agent.address}")
    ctx.logger.info(f"And wallet address: {chatbot_agent.wallet.address()}")

@chatbot_agent.on_query(model=UserRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: UserRequest):
    user_address = sender
    query = _query.query
    try:
        # Load data from JSON file
        data = load_json_data()
        
        if data:
            # Extract data for response
            summary = data.get("summary")
            location = data.get("location")
            soil_data = data.get("soil_data", [])
            population = data.get("population")
            poverty = data.get("poverty")
            land_percentage = data.get("land_percentage")
            drought_percentage = data.get("drought_percentage")
            ctx.logger.info("here")

            # Construct response based on the extracted data
            response = chatbot_query(
                summary=summary,
                location=location,
                query=query,
                soil_data=soil_data,
                population=population,
                poverty=poverty,
                land_percentage=land_percentage,
                drought_percentage=drought_percentage
            )
            ctx.logger.info(f"response {response}")
            
            with open("response.json", "w") as f:
                json.dump(response, f, indent=4)
        else:
            response = "Please select a location within a city."
            with open("response.json", "w") as f:
                json.dump(response, f, indent=4)
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

if __name__ == "__main__":
    chatbot_agent.run()