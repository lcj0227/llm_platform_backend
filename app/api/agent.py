from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.agent import AgentCreate, AgentUpdate, AgentOut
from app.services import agent_service
from app.db.session import get_db

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/", response_model=AgentOut)
def create_agent(data: AgentCreate, db: Session = Depends(get_db)):
    return agent_service.create_agent(db, data)

@router.get("/", response_model=list[AgentOut])
def list_agents(db: Session = Depends(get_db)):
    return agent_service.get_agents(db)

@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = agent_service.get_agent_by_id(db, agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: str, data: AgentUpdate, db: Session = Depends(get_db)):
    updated = agent_service.update_agent(db, agent_id, data)
    if not updated:
        raise HTTPException(404, "Agent not found")
    return updated

@router.delete("/{agent_id}")
def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    result = agent_service.delete_agent(db, agent_id)
    if not result:
        raise HTTPException(404, "Agent not found")
    return {"message": "Deleted"}

@router.get("/mcp/{mcp_id}", response_model=list[AgentOut])
def get_agents_by_mcp(mcp_id: str, db: Session = Depends(get_db)):
    return agent_service.get_agents_by_mcp(db, mcp_id) 