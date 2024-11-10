 
import json
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import UserRequest, Response
from agent_funcs import drought_risk_percentage, get_economist_data, land_degradation_risk_percentage, chatbot_query, risk_summary, generate_soil_data_predictions, predict_land_percentage, predict_drought_percentage, generate_summary_prediction
from api.location import get_address_from_coords, get_population_from_coords, get_poverty_from_coords 
from api.weather import get_soil_data
from agent_funcs import drought_risk_percentage, land_degradation_risk_percentage, chatbot_query, risk_summary
from api.weather import get_soil_data
from uagents.setup import fund_agent_if_low

load_dotenv()
 
# Initialize the agent with its configuration.
environmentalist_agent = Agent(
    name="Risk Analyzer Agent",
    seed="Risk Analyzer Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(environmentalist_agent.wallet.address())

 
@environmentalist_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {environmentalist_agent.name}")
    ctx.logger.info(f"With address: {environmentalist_agent.address}")
    ctx.logger.info(f"And wallet address: {environmentalist_agent.wallet.address()}")
 
# Decorator to handle incoming queries.
@environmentalist_agent.on_query(model=UserRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: UserRequest):
    ctx.logger.info(f"there", )
    user_address = sender
    ctx.logger.info(f"heree")
    ctx.logger.info(f"Query received by the risk analyzer : {user_address}")

    try:
        response_land_data = get_soil_data(_query.lat, _query.lon)
        location = get_address_from_coords(_query.lat, _query.lon)   
        population = get_population_from_coords(_query.lat, _query.lon)
        poverty = get_poverty_from_coords(_query.lat, _query.lon)

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

        await ctx.send(ECONOMIST_AGENT_ADDRESS, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

economist_agent = Agent(
    name="Economist Agent",
    seed="Economist Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)
fund_agent_if_low(economist_agent.wallet.address())

ECONOMIST_AGENT_ADDRESS = "agent1qdupymd2lvhh5rzsnatch6chprejg9d9jhff9xavqnesft2qyndjv2qudce"

@economist_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {economist_agent.name}")
    ctx.logger.info(f"With address: {economist_agent.address}")
    ctx.logger.info(f"And wallet address: {economist_agent.wallet.address()}")

@economist_agent.on_query(model=Response)
async def query_handler(ctx: Context, sender: str, message: Response):
    ctx.logger.info(f"Economist agent received query from {sender}")

    try:
        # Read location data from the message or state file
        with open("state.json", "r") as f:
            state_data = json.load(f)

        location = state_data.get("location", "unknown")

        economist_data_list = get_economist_data(location)
        if not economist_data_list or len(economist_data_list) < 7:
            raise ValueError("Incomplete data returned from get_economist_data")

        # Compile data into a response JSON
        economist_data = {
            "location": economist_data_list[0],
            "vegetation_level": economist_data_list[1],
            "average_salary": economist_data_list[2],
            "food_price_percentage": economist_data_list[3],
            "migration_patterns": economist_data_list[4],
            "economic_diversity": economist_data_list[5],
            "graduation_rate": economist_data_list[6]
        }

        ctx.logger.info(f"Compiled economist data: {economist_data}")

        # Save economist data to a JSON file (optional)
        with open("economist_data.json", "w") as f:
            json.dump(economist_data, f, indent=4)  

        # Send response back to the sender
        await ctx.send(PREDICTOR_AGENT_ADDRESS, Response(text="success"))

    except Exception as e:
        # Handle errors and send a failure response
        ctx.logger.error(f"Error generating economist data: {e}")
        await ctx.send(sender, Response(text="An error occurred while generating economist data."))

predictor_agent = Agent(
    name="Predictor Agent",
    seed="Predictor Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(predictor_agent.wallet.address())

PREDICTOR_AGENT_ADDRESS = "agent1qwxe5ktzqqjk8g48nj3h3mhz3gg43wte37ejj8vtncs99sm6yyxsy2p0g0k"

@predictor_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {predictor_agent.name}")
    ctx.logger.info(f"With address: {predictor_agent.address}")
    ctx.logger.info(f"And wallet address: {predictor_agent.wallet.address()}")

@predictor_agent.on_query(model=Response)
async def query_handler(ctx: Context, sender: str, message: Response):
    ctx.logger.info(f"Predictor agent received query from {sender}")
    try:
        # Read the state data
        with open("state.json", "r") as f:
            state_data = json.load(f)
            
        # Initialize prediction JSON with static values
        prediction_json = {
            "location": state_data["location"],
            "population": state_data["population"],
            "poverty": state_data["poverty"]
        }

        ctx.logger.info(f"Initialized prediction_json: {prediction_json}")
        
        # Generate predictions for each section
        prediction_json["soil_data"] = await generate_soil_data_predictions(state_data["soil_data"])
        ctx.logger.info(f"Generated soil_data predictions: {prediction_json['soil_data']}")
        prediction_json["land_percentage"] = predict_land_percentage(state_data["land_percentage"])
        ctx.logger.info(f"Generated land_percentage predictions: {prediction_json['land_percentage']}")
        prediction_json["drought_percentage"] = predict_drought_percentage(state_data["drought_percentage"])
        ctx.logger.info(f"Generated drought_percentage predictions: {prediction_json['drought_percentage']}")
        prediction_json["summary"] = await generate_summary_prediction(
            state_data["summary"],
            prediction_json["soil_data"],
            prediction_json["land_percentage"],
            prediction_json["drought_percentage"]
        )
        ctx.logger.info(f"Generated summary prediction: {prediction_json['summary']}")

        # Write the prediction JSON to future-state.json
        with open("future-state.json", "w") as f:
            json.dump(prediction_json, f, indent=4)

        # Send a success response back
        ctx.send("agent1qfyv0rdcq6qzsa9rylulryuzaxj3xc6sdp8xfl8wdh97fdxmpm027qyyedu", Response(text="success"))

    except Exception as e:
        # Log any errors and send a failure response
        ctx.logger.error(f"Error generating prediction JSON: {e}")
        await ctx.send(sender, Response(text="An error occurred while generating the prediction JSON."))


bureau = Bureau(port=8001, endpoint=["http://127.0.0.1:8001/submit"])
bureau.add(environmentalist_agent)
bureau.add(predictor_agent)
bureau.add(economist_agent)

# Main execution block to run the agent.
if __name__ == "__main__":
    bureau.run()