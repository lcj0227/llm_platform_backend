from fastapi import FastAPI
from app.api import mcp, agent, ai_app
from app.db.session import init_db

app = FastAPI()
app.include_router(mcp.router)
app.include_router(agent.router)
app.include_router(ai_app.router)

@app.on_event("startup")
def startup():
    init_db()
