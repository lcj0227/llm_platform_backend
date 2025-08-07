from sqlalchemy.orm import Session
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate
import json

def create_agent(db: Session, data: AgentCreate):
    db_agent = Agent(
        id=data.id,
        name=data.name,
        description=data.description,
        system_prompt=data.system_prompt,
        temperature=data.temperature,
        max_tokens=data.max_tokens,
        is_active=data.is_active,
        mcp_id=data.mcp_id,
        tools=json.dumps(data.tools)
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_agents(db: Session):
    return db.query(Agent).all()

def get_agent_by_id(db: Session, agent_id: str):
    return db.query(Agent).filter(Agent.id == agent_id).first()

def update_agent(db: Session, agent_id: str, data: AgentUpdate):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        return None
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "tools":
            setattr(db_agent, field, json.dumps(value))
        else:
            setattr(db_agent, field, value)
    
    db.commit()
    db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: str):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        return None
    db.delete(db_agent)
    db.commit()
    return True

def get_agents_by_mcp(db: Session, mcp_id: str):
    return db.query(Agent).filter(Agent.mcp_id == mcp_id).all() 