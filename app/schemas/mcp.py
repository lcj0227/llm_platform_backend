from pydantic import BaseModel, Field, validator
from typing import List, Optional
import json

class MCPCreate(BaseModel):
    id: str
    name: str
    provider: str
    model: str
    temperature: Optional[str] = "0.7"
    api_key: str
    tool_plugins: Optional[List[str]] = []

class MCPUpdate(BaseModel):
    name: Optional[str]
    model: Optional[str]
    temperature: Optional[str]
    api_key: Optional[str]
    tool_plugins: Optional[List[str]]

class MCPOut(BaseModel):
    id: str
    name: str
    provider: str
    model: str
    temperature: str
    tool_plugins: List[str]

    @validator('tool_plugins', pre=True)
    def parse_tool_plugins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v if v is not None else []

    class Config:
        orm_mode = True
