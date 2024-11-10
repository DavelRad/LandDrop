 
import json
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import UserRequest, Response
from agent_funcs import drought_risk_percentage, land_degradation_risk_percentage, chatbot_query, risk_summary
from api.functions import get_address_from_coords, get_soil_data, get_population_data, get_poverty_data, generate_soil_data_predictions, predict_land_percentage, predict_drought_percentage, generate_summary_prediction
from uagents.setup import fund_agent_if_low

load_dotenv()
 
# Initialize the agent with its configuration.
analyzer_agent = Agent(
    name="Risk Analyzer Agent",
    seed="Risk Analyzer Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(analyzer_agent.wallet.address())

 
@analyzer_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {analyzer_agent.name}")
    ctx.logger.info(f"With address: {analyzer_agent.address}")
    ctx.logger.info(f"And wallet address: {analyzer_agent.wallet.address()}")
 
# Decorator to handle incoming queries.
@analyzer_agent.on_query(model=UserRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: UserRequest):
    ctx.logger.info(f"there", )
    user_address = sender
    ctx.logger.info(f"heree")
    ctx.logger.info(f"Query received by the risk analyzer : {user_address}")

    try:
        response_land_data = get_soil_data(_query.lat, _query.lon)
        location = get_address_from_coords(_query.lat, _query.lon)   
        population = get_population_data(_query.lat, _query.lon)
        poverty = get_poverty_data(_query.lat, _query.lon)

        land_percentage_response = land_degradation_risk_percentage(response_land_data["data"])
        drought_percentage_response = drought_risk_percentage(response_land_data["data"])

        land_percentage = [int(value) for value in land_percentage_response.split(",")]
        drought_percentage = [int(value) for value in drought_percentage_response.split(",")]

        data = {
            "location": location,
            "soil_data": response_land_data["data"],
            "population": population,
            "poverty": poverty,
            "land_percentage": land_percentage,
            "drought_percentage": drought_percentage,
        }

        # Generate summary if needed
        summary = risk_summary(data)
        data["summary"] = summary
    

        ctx.logger.info(f"population: {population}")
        ctx.logger.info(f"poverty: {poverty}")
        ctx.logger.info(f"response_land_data: {response_land_data}")
        ctx.logger.info(f"land_percentage: {land_percentage}")
        ctx.logger.info(f"drought_percentage: {drought_percentage}")

        with open("state.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

 
predictor_agent = Agent(
    name="Predictor Agent",
    seed="Predictor Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

PREDICTOR_AGENT_ADDRESS = "agent1qwxe5ktzqqjk8g48nj3h3mhz3gg43wte37ejj8vtncs99sm6yyxsy2p0g0k"

@predictor_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {predictor_agent.name}")
    ctx.logger.info(f"With address: {predictor_agent.address}")
    ctx.logger.info(f"And wallet address: {predictor_agent.wallet.address()}")

@predictor_agent.on_query(model=UserRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: UserRequest):
    ctx.logger.info(f"Predictor agent received query from {sender}")
    with open("state.json", "r") as f:
        state_data = json.load(f)
    prediction_json = {
        "location": state_data["location"],
        "population": state_data["population"],
        "poverty": state_data["poverty"]
    }

    # Helper functions to process and predict each section of data
    prediction_json["soil_data"] = await generate_soil_data_predictions(state_data["soil_data"])
    prediction_json["land_percentage"] = await predict_land_percentage(state_data["soil_data"],state_data["land_percentage"])
    prediction_json["drought_percentage"] = await predict_drought_percentage(state_data["drought_percentage"])
    prediction_json["summary"] = await generate_summary_prediction(state_data["summary"])

    # Save prediction JSON to future-state.json
    with open("future-state.json", "w") as f:
        json.dump(prediction_json, f, indent=4)

    # Send a response back
    await ctx.send(sender, Response(text="Prediction JSON generated successfully."))

bureau = Bureau(port=8001, endpoint=["http://127.0.0.1:8001/submit"])
bureau.add(analyzer_agent)
bureau.add(predictor_agent)

# Main execution block to run the agent.
if __name__ == "__main__":
    bureau.run()
    