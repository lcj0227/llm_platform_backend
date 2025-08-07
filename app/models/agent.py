from sqlalchemy import Column, String, Text, VARCHAR, Boolean
from app.db.session import Base

class Agent(Base):
    __tablename__ = "agent"

    id = Column(VARCHAR(255), primary_key=True, index=True)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text)
    system_prompt = Column(Text, nullable=False)
    temperature = Column(VARCHAR(10), default="0.7")
    max_tokens = Column(VARCHAR(10), default="4000")
    is_active = Column(Boolean, default=True)
    mcp_id = Column(VARCHAR(255), nullable=False)  # 关联的MCP ID
    tools = Column(Text)  # 可存 JSON 字符串，存储工具配置 