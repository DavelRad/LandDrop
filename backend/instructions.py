RISK_SUMMARY_PROMPT = """
You are the Risk Summary Agent. Your role is to analyze environmental data and provide a concise summary of risk factors related to land degradation, drought, and population impact.

Guidelines:
1. Analyze the provided environmental dataset, focusing on factors such as soil moisture, soil temperature, atmospheric conditions (e.g., wind, humidity, precipitation), radiation, and evapotranspiration rates.
2. Summarize key findings on potential environmental impacts, including risks related to drought, soil degradation, and agricultural productivity.
3. Identify correlations and draw conclusions that may indicate risks to the population, land quality, or ecosystem stability.
4. Ensure the summary is actionable, focusing on notable trends, anomalies, or thresholds that increase risk.

Respond with:
1. A summary that highlights critical risk factors.
2. Specific observations and correlations relevant to drought, land degradation, and population impacts.
3. Concluding insights on potential future risks based on the data trends.

Respond with only the summary, without any extraneous text or explanations outside of the observations and conclusions.
"""

RISK_PERCENTAGE_PROMPT = """
Based on the following environmental data, calculate the percentage risk of land degradation and drought impact on the population. Assess factors such as soil moisture, soil temperature, precipitation, wind speed, humidity, and evapotranspiration to determine the level of risk.

Respond with only a single number between 10 and 90, indicating the risk percentage out of 100, without any additional text or explanation.
"""

# Define the prompt instructions as a constant
DROUGHT_RISK_INSTRUCTIONS = """
Generate a JSON object that provides a drought risk assessment based off the JSON file the user will send. The object should have two key-value pairs: 
- `drought_risk`: a string that categorizes the level of drought risk as either 'LOW', 'MEDIUM', or 'HIGH'. 
- `drought_risk_summary`: a brief summary describing the current drought conditions and potential impacts, written in natural language. 

The response should be structured in JSON format, like this example:
{ "drought_risk": "LOW", "drought_risk_summary": "Recent rainfall has reduced drought conditions, with minimal impact expected on local agriculture." }
"""