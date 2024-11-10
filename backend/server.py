 
import json
from fastapi import FastAPI, Request
from uagents import Model
from agent_class import UserRequest
from uagents.query import query
from uagents.envelope import Envelope
from fastapi.middleware.cors import CORSMiddleware


 
AGENT_ADDRESS = "agent1qfyv0rdcq6qzsa9rylulryuzaxj3xc6sdp8xfl8wdh97fdxmpm027qyyedu"
CHATBOT_ADDRESS= ""

origins = [
    "http://localhost:3000",  # Your React app's origin
]
 
 
async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    print(req)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response
 
async def chatbot_agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    print(req)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response
 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)
 
@app.get("/")
def read_root():
    return "Hello from the Agent controller"
 
@app.post("/endpoint")
async def make_agent_call(req: Request):
    model = UserRequest.parse_obj(await req.json())
    #print(model)
    try:
        res = await agent_query(model)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"
 
@app.post("/chatbot")
async def make_agent_call(req: Request):
    model = UserRequest.parse_obj(await req.json())
    try:
        res = await agent_query(model)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"
 