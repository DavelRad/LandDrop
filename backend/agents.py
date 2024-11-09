 
from dotenv import load_dotenv
from uagents import Agent, Context, Model, Bureau
from agent_class import Request, Response

load_dotenv()
 
# Initialize the agent with its configuration.
risk_analyzer_agent = Agent(
    name="Risk Analyzer Agent",
    seed="Risk Analyzer Secret Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)
 
@risk_analyzer_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {risk_analyzer_agent.name}")
    ctx.logger.info(f"With address: {risk_analyzer_agent.address}")
    ctx.logger.info(f"And wallet address: {risk_analyzer_agent.wallet.address()}")
 
# Decorator to handle incoming queries.
@risk_analyzer_agent.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Request):
    ctx.logger.info("Query received")
    try:
        # do something here
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))
 
bureau = Bureau(port=8001)
bureau.add(risk_analyzer_agent)

# Main execution block to run the agent.
if __name__ == "__main__":
    bureau.run()
    