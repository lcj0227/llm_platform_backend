from sqlalchemy import Column, String, Text, VARCHAR, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class AIApp(Base):
    __tablename__ = "ai_app"

    id = Column(VARCHAR(255), primary_key=True, index=True)
    name = Column(VARCHAR(255), nullable=False, comment="应用名称")
    identifier = Column(VARCHAR(255), nullable=False, unique=True, comment="应用标识符")
    icon = Column(VARCHAR(500), comment="应用图标URL")
    description = Column(Text, comment="应用描述")
    is_active = Column(Boolean, default=True, comment="启用状态")
    dashboard_url = Column(VARCHAR(500), comment="默认Dashboard地址")
    access_url = Column(VARCHAR(500), comment="独立访问URL")
    
    # Agent配置
    main_agent_id = Column(VARCHAR(255), comment="主Agent ID，null表示使用默认Agent")
    agent_list = Column(Text, comment="Agent列表，JSON格式存储")
    
    # MCP配置
    mcp_list = Column(Text, comment="MCP列表，JSON格式存储")
    
    # 系统配置
    llm_config = Column(Text, comment="大模型配置，JSON格式存储")
    system_prompt = Column(Text, comment="系统提示词")
    
    # 应用类型
    app_type = Column(VARCHAR(50), default="platform", comment="应用类型：platform-平台应用，user-我的应用")
    user_id = Column(VARCHAR(255), comment="创建用户ID，平台应用为null")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 