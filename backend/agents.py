 
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import UserRequest, Response
from agent_funcs import risk_summary, risk_percentage
from api.weather import get_soil_data
from uagents.setup import fund_agent_if_low

load_dotenv()
 
# Initialize the agent with its configuration.
risk_analyzer_agent = Agent(
    name="Risk Analyzer Agent",
    seed="Risk Analyzer Secret Phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(risk_analyzer_agent.wallet.address())

 
@risk_analyzer_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {risk_analyzer_agent.name}")
    ctx.logger.info(f"With address: {risk_analyzer_agent.address}")
    ctx.logger.info(f"And wallet address: {risk_analyzer_agent.wallet.address()}")
 
# Decorator to handle incoming queries.
@risk_analyzer_agent.on_query(model=UserRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: UserRequest):
    ctx.logger.info(f"there", )
    user_address = sender
    ctx.logger.info(f"heree")
    ctx.logger.info(f"Query received by the risk analyzer : {user_address}")

    try:
        response_land_data = get_soil_data(_query.lat, _query.lon)
        summary = risk_summary(response_land_data)
        percentage = risk_percentage(response_land_data, summary)
        ctx.logger.info(f"response_land_data: {response_land_data}")
        ctx.logger.info(f"summary: {summary}")
        ctx.logger.info(f"percentage: {percentage}")
        await ctx.send(sender, Response(text="success", land_data=response_land_data, summary=summary, risk_percentage=int(percentage)))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

 
bureau = Bureau(port=8001, endpoint=["http://127.0.0.1:8001/submit"])
bureau.add(risk_analyzer_agent)

# Main execution block to run the agent.
if __name__ == "__main__":
    bureau.run()
    