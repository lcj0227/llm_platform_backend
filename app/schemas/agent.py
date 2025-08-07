from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import json

class AgentCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    system_prompt: str
    temperature: Optional[str] = "0.7"
    max_tokens: Optional[str] = "4000"
    is_active: Optional[bool] = True
    mcp_id: str
    tools: Optional[List[Dict[str, Any]]] = []

class AgentUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    system_prompt: Optional[str]
    temperature: Optional[str]
    max_tokens: Optional[str]
    is_active: Optional[bool]
    mcp_id: Optional[str]
    tools: Optional[List[Dict[str, Any]]]

class AgentOut(BaseModel):
    id: str
    name: str
    description: str
    system_prompt: str
    temperature: str
    max_tokens: str
    is_active: bool
    mcp_id: str
    tools: List[Dict[str, Any]]

    @validator('tools', pre=True)
    def parse_tools(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v if v is not None else []

    class Config:
        orm_mode = True 