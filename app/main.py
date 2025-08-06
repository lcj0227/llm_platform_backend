from fastapi import FastAPI
from app.api import mcp
from app.db.session import init_db

app = FastAPI()
app.include_router(mcp.router)

@app.on_event("startup")
def startup():
    init_db()
