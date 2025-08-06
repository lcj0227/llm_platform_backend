from sqlalchemy import Column, String, Text, VARCHAR
from app.db.session import Base

class MCP(Base):
    __tablename__ = "mcp"

    id = Column(VARCHAR(255), primary_key=True, index=True)
    name = Column(VARCHAR(255), nullable=False)
    provider = Column(VARCHAR(100), nullable=False)  # openai, azure, etc.
    model = Column(VARCHAR(100), nullable=False)     # gpt-3.5-turbo, etc.
    temperature = Column(VARCHAR(10), default="0.7")
    api_key = Column(Text, nullable=False)
    tool_plugins = Column(Text)  # 可存 JSON 字符串
