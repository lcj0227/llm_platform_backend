from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# MCP配置Schema
class MCPConfig(BaseModel):
    mcp_id: str
    name: str
    description: str
    custom_description: Optional[str] = None

# Agent配置Schema
class AgentConfig(BaseModel):
    agent_id: str
    name: str
    description: Optional[str] = None

# 大模型配置Schema
class LLMConfig(BaseModel):
    provider: str  # openai, azure, etc.
    model: str     # gpt-3.5-turbo, etc.
    temperature: float = 0.7
    max_tokens: int = 4000
    api_key: Optional[str] = None

# AI应用基础配置Schema
class AIAppBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="应用名称")
    identifier: str = Field(..., min_length=1, max_length=255, description="应用标识符")
    icon: Optional[str] = Field(None, max_length=500, description="应用图标URL")
    description: Optional[str] = Field(None, description="应用描述")
    is_active: bool = Field(True, description="启用状态")
    dashboard_url: Optional[str] = Field(None, max_length=500, description="默认Dashboard地址")
    
    # Agent配置
    main_agent_id: Optional[str] = Field(None, description="主Agent ID，null表示使用默认Agent")
    agent_list: Optional[List[AgentConfig]] = Field(None, description="Agent列表")
    
    # MCP配置
    mcp_list: Optional[List[MCPConfig]] = Field(None, description="MCP列表")
    
    # 系统配置
    llm_config: Optional[List[LLMConfig]] = Field(None, description="大模型配置")
    system_prompt: Optional[str] = Field(None, description="系统提示词")

# 创建AI应用Schema
class AIAppCreate(AIAppBase):
    app_type: str = Field("platform", description="应用类型：platform-平台应用，user-我的应用")
    user_id: Optional[str] = Field(None, description="创建用户ID，平台应用为null")

# 更新AI应用Schema
class AIAppUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="应用名称")
    identifier: Optional[str] = Field(None, min_length=1, max_length=255, description="应用标识符")
    icon: Optional[str] = Field(None, max_length=500, description="应用图标URL")
    description: Optional[str] = Field(None, description="应用描述")
    is_active: Optional[bool] = Field(None, description="启用状态")
    dashboard_url: Optional[str] = Field(None, max_length=500, description="默认Dashboard地址")
    
    # Agent配置
    main_agent_id: Optional[str] = Field(None, description="主Agent ID，null表示使用默认Agent")
    agent_list: Optional[List[AgentConfig]] = Field(None, description="Agent列表")
    
    # MCP配置
    mcp_list: Optional[List[MCPConfig]] = Field(None, description="MCP列表")
    
    # 系统配置
    llm_config: Optional[List[LLMConfig]] = Field(None, description="大模型配置")
    system_prompt: Optional[str] = Field(None, description="系统提示词")

# AI应用响应Schema
class AIAppResponse(AIAppBase):
    id: str
    access_url: Optional[str] = Field(None, description="独立访问URL")
    app_type: str
    user_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI应用列表响应Schema
class AIAppListResponse(BaseModel):
    apps: List[AIAppResponse]
    total: int
    page: int
    size: int

# 生成系统提示词请求Schema
class GenerateSystemPromptRequest(BaseModel):
    app_name: str
    app_description: Optional[str] = None
    agent_list: Optional[List[AgentConfig]] = None
    mcp_list: Optional[List[MCPConfig]] = None 