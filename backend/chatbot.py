import json
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from agent_class import UserRequest, Response
from agent_funcs import chatbot_query, risk_summary
from api.weather import get_soil_data
from uagents.setup import fund_agent_if_low

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
def load_chat_history():
    """Load existing chat history from chat.json if it exists and ensure it's a list."""
    try:
        with open("chat.json", "r") as f:
            history = json.load(f)
            if not isinstance(history, list):
                history = []
            return history
    except FileNotFoundError:
        return []  # Start with an empty history if file doesn't exist

def save_chat_history(history):
    """Save updated chat history to chat.json."""
    with open("chat.json", "w") as f:
        json.dump(history, f, indent=4)

def format_history(history):
    """Format chat history for context in the prompt."""
    formatted_history = "\n".join([f"User: {entry['query']}\nAssistant: {entry['response']}" for entry in history])
    return formatted_history
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

        # Load existing chat history for context
        chat_history = load_chat_history()
        formatted_history = format_history(chat_history)

        if data:
            # Extract data for response
            summary = data.get("summary")
            location = data.get("location")
            soil_data = data.get("soil_data", [])
            population = data.get("population")
            poverty = data.get("poverty")
            land_percentage = data.get("land_percentage")
            drought_percentage = data.get("drought_percentage")

            # Construct response based on the extracted data
            response = chatbot_query(
                summary=summary,
                location=location,
                query=query,
                soil_data=soil_data,
                population=population,
                poverty=poverty,
                land_percentage=land_percentage,
                drought_percentage=drought_percentage,
                chat_history=formatted_history
            )
            
            # Append new query and response to chat history
            chat_history.append({
                "query": query,
                "response": response,
                "user": user_address
            })
            
            # Save updated chat history
            save_chat_history(chat_history)

            ctx.logger.info(f"response {response}")
        else:
            # No data found; provide default response
            response = "Please select a location within a city."
            chat_history.append({"query": query, "response": response, "user": user_address})
            save_chat_history(chat_history)
        
        await ctx.send(sender, Response(text="success"))
    except Exception as e:
        ctx.logger.error(f"Error in query_handler: {e}")
        await ctx.send(sender, Response(text="fail"))

if __name__ == "__main__":
    chatbot_agent.run()
