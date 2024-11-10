 
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from uagents import Model
from agent_class import UserRequest
from uagents.query import query
from uagents.envelope import Envelope
from fastapi.middleware.cors import CORSMiddleware
import os

 
AGENT_ADDRESS = "agent1qfyv0rdcq6qzsa9rylulryuzaxj3xc6sdp8xfl8wdh97fdxmpm027qyyedu"
CHATBOT_ADDRESS= "agent1qtu8y0899lru8x9mm60zf2v07q9uqe4l4rc07e82rrss4hsa3tqjvrt6276"

origins = [
    "http://localhost:3000",  # Your React app's origin
]


 
class TestRequest(Model):
    message: str
    lat: float
    lon: float
    user: str = None
 
async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    print(req)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response
 
async def chatbot_agent_query(req):
    response = await query(destination=CHATBOT_ADDRESS, message=req, timeout=15)
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
    try:

        if os.path.exists('chat.json'):
            os.remove('chat.json')
        res = await agent_query(model)
        with open('state.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception:
        return "unsuccessful agent call"
 
@app.post("/chatbot")
async def make_agent_call(req: Request):
    model = UserRequest.parse_obj(await req.json())
    try:
        res = await chatbot_agent_query(model)
        with open('chat.json', 'r') as file:
            data = json.load(file)
        response = data[-1]["response"]
        return response
    except Exception as e:
        return {"status": "error", "message": "Unsuccessful agent call", "details": str(e)}
    
@app.post("/endpoint2")
async def get_file():
    try:
        with open('future-state.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {"status": "error", "message": "Unsuccessful agent call", "details": str(e)}
    
@app.post("/endpoint3")
async def get_file():
    try:
        with open('economist_data.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {"status": "error", "message": "Unsuccessful agent call", "details": str(e)}