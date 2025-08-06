from sqlalchemy.orm import Session
from app.models.mcp import MCP
from app.schemas.mcp import MCPCreate, MCPUpdate
import json

def create_mcp(db: Session, data: MCPCreate):
    db_mcp = MCP(
        id=data.id,
        name=data.name,
        provider=data.provider,
        model=data.model,
        temperature=data.temperature,
        api_key=data.api_key,
        tool_plugins=json.dumps(data.tool_plugins)
    )
    db.add(db_mcp)
    db.commit()
    db.refresh(db_mcp)
    return db_mcp

def get_mcps(db: Session):
    return db.query(MCP).all()

def update_mcp(db: Session, mcp_id: str, data: MCPUpdate):
    db_mcp = db.query(MCP).filter(MCP.id == mcp_id).first()
    if not db_mcp:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        if field == "tool_plugins":
            setattr(db_mcp, field, json.dumps(value))
        else:
            setattr(db_mcp, field, value)
    db.commit()
    db.refresh(db_mcp)
    return db_mcp

def delete_mcp(db: Session, mcp_id: str):
    db_mcp = db.query(MCP).filter(MCP.id == mcp_id).first()
    if not db_mcp:
        return None
    db.delete(db_mcp)
    db.commit()
    return True
