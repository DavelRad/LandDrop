from uagents import Model
from typing import Any, Optional

class Request(Model):
    query: str
    lat: float 
    lon: float
    user: str = None

class Response(Model):
    text: str
    land_data: Optional[dict] = None
    summary: Optional[str] = None
    risk_percentage: Optional[int] = None

    class Config:
        # Include fields with None values during serialization
        exclude_none = False