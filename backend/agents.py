 
import json
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import UserRequest, Response
from agent_funcs import drought_risk_percentage, land_degradation_risk_percentage, chatbot_query, risk_summary
from api.functions import get_address_from_coords, get_soil_data, get_population_data, get_poverty_data
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
        land_percentage = land_degradation_risk_percentage(response_land_data)
        drought_percentage = drought_risk_percentage(response_land_data)
        data = {} 
        data["location"] = location
        data["soil_data"] = response_land_data["data"]
        data["population"] = population
        data["poverty"] = poverty
        summary = risk_summary(data)
        data["land_percentage"] = land_degradation_risk_percentage(response_land_data)
        data["drought_percentage"] = drought_risk_percentage(response_land_data)
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

 
bureau = Bureau(port=8001, endpoint=["http://127.0.0.1:8001/submit"])
bureau.add(analyzer_agent)

# Main execution block to run the agent.
if __name__ == "__main__":
    bureau.run()
    