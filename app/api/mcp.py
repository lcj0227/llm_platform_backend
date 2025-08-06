from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.mcp import MCPCreate, MCPUpdate, MCPOut
from app.services import mcp_service
from app.db.session import get_db

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.post("/", response_model=MCPOut)
def create_mcp(data: MCPCreate, db: Session = Depends(get_db)):
    return mcp_service.create_mcp(db, data)

@router.get("/", response_model=list[MCPOut])
def list_mcps(db: Session = Depends(get_db)):
    return mcp_service.get_mcps(db)

@router.put("/{mcp_id}", response_model=MCPOut)
def update_mcp(mcp_id: str, data: MCPUpdate, db: Session = Depends(get_db)):
    updated = mcp_service.update_mcp(db, mcp_id, data)
    if not updated:
        raise HTTPException(404, "MCP not found")
    return updated

@router.delete("/{mcp_id}")
def delete_mcp(mcp_id: str, db: Session = Depends(get_db)):
    result = mcp_service.delete_mcp(db, mcp_id)
    if not result:
        raise HTTPException(404, "MCP not found")
    return {"message": "Deleted"}
