import json
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.ai_app import AIApp
from app.models.agent import Agent
from app.models.mcp import MCP
from app.schemas.ai_app import (
    AIAppCreate, 
    AIAppUpdate, 
    AIAppResponse, 
    GenerateSystemPromptRequest,
    AgentConfig,
    MCPConfig,
    LLMConfig
)

class AIAppService:
    
    @staticmethod
    def create_ai_app(db: Session, ai_app_data: AIAppCreate) -> AIAppResponse:
        """创建AI应用"""
        # 生成唯一ID
        app_id = str(uuid.uuid4())
        
        # 生成独立访问URL
        access_url = f"/app/{ai_app_data.identifier}"
        
        # 处理JSON字段
        agent_list_json = None
        if ai_app_data.agent_list:
            agent_list_json = json.dumps([agent.dict() for agent in ai_app_data.agent_list])
        
        mcp_list_json = None
        if ai_app_data.mcp_list:
            mcp_list_json = json.dumps([mcp.dict() for mcp in ai_app_data.mcp_list])
        
        llm_config_json = None
        if ai_app_data.llm_config:
            llm_config_json = json.dumps([llm.dict() for llm in ai_app_data.llm_config])
        
        # 创建AI应用
        db_ai_app = AIApp(
            id=app_id,
            name=ai_app_data.name,
            identifier=ai_app_data.identifier,
            icon=ai_app_data.icon,
            description=ai_app_data.description,
            is_active=ai_app_data.is_active,
            dashboard_url=ai_app_data.dashboard_url,
            access_url=access_url,
            main_agent_id=ai_app_data.main_agent_id,
            agent_list=agent_list_json,
            mcp_list=mcp_list_json,
            llm_config=llm_config_json,
            system_prompt=ai_app_data.system_prompt,
            app_type=ai_app_data.app_type,
            user_id=ai_app_data.user_id
        )
        
        db.add(db_ai_app)
        db.commit()
        db.refresh(db_ai_app)
        
        return AIAppService._convert_to_response(db_ai_app)
    
    @staticmethod
    def get_ai_app(db: Session, app_id: str) -> Optional[AIAppResponse]:
        """获取单个AI应用"""
        db_ai_app = db.query(AIApp).filter(AIApp.id == app_id).first()
        if not db_ai_app:
            return None
        return AIAppService._convert_to_response(db_ai_app)
    
    @staticmethod
    def get_ai_apps(
        db: Session, 
        app_type: Optional[str] = None,
        user_id: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> Dict[str, Any]:
        """获取AI应用列表"""
        query = db.query(AIApp)
        
        # 根据应用类型过滤
        if app_type:
            query = query.filter(AIApp.app_type == app_type)
        
        # 根据用户ID过滤
        if user_id:
            query = query.filter(AIApp.user_id == user_id)
        
        total = query.count()
        db_ai_apps = query.offset(skip).limit(limit).all()
        
        apps = [AIAppService._convert_to_response(app) for app in db_ai_apps]
        
        return {
            "apps": apps,
            "total": total,
            "page": skip // limit + 1,
            "size": limit
        }
    
    @staticmethod
    def update_ai_app(db: Session, app_id: str, ai_app_data: AIAppUpdate) -> Optional[AIAppResponse]:
        """更新AI应用"""
        db_ai_app = db.query(AIApp).filter(AIApp.id == app_id).first()
        if not db_ai_app:
            return None
        
        # 更新字段
        update_data = ai_app_data.dict(exclude_unset=True)
        
        # 处理JSON字段
        if "agent_list" in update_data:
            update_data["agent_list"] = json.dumps([agent.dict() for agent in update_data["agent_list"]])
        
        if "mcp_list" in update_data:
            update_data["mcp_list"] = json.dumps([mcp.dict() for mcp in update_data["mcp_list"]])
        
        if "llm_config" in update_data:
            update_data["llm_config"] = json.dumps([llm.dict() for llm in update_data["llm_config"]])
        
        # 更新独立访问URL
        if "identifier" in update_data:
            update_data["access_url"] = f"/app/{update_data['identifier']}"
        
        for field, value in update_data.items():
            setattr(db_ai_app, field, value)
        
        db.commit()
        db.refresh(db_ai_app)
        
        return AIAppService._convert_to_response(db_ai_app)
    
    @staticmethod
    def delete_ai_app(db: Session, app_id: str) -> bool:
        """删除AI应用"""
        db_ai_app = db.query(AIApp).filter(AIApp.id == app_id).first()
        if not db_ai_app:
            return False
        
        db.delete(db_ai_app)
        db.commit()
        return True
    
    @staticmethod
    def generate_system_prompt(request: GenerateSystemPromptRequest) -> str:
        """自动生成系统提示词"""
        prompt_parts = []
        
        # 基础信息
        prompt_parts.append(f"你是一个名为'{request.app_name}'的AI应用。")
        
        if request.app_description:
            prompt_parts.append(f"应用描述：{request.app_description}")
        
        # Agent信息
        if request.agent_list:
            agent_names = [agent.name for agent in request.agent_list]
            prompt_parts.append(f"可用的Agent：{', '.join(agent_names)}")
        
        # MCP信息
        if request.mcp_list:
            mcp_names = [mcp.name for mcp in request.mcp_list]
            prompt_parts.append(f"可用的MCP工具：{', '.join(mcp_names)}")
        
        # 系统行为指导
        prompt_parts.append("""
请根据用户的需求，合理调度和使用可用的Agent和MCP工具来完成任务。
确保回答准确、有用，并充分利用可用的工具资源。
""")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def get_available_agents(db: Session) -> List[Dict[str, Any]]:
        """获取可用的Agent列表"""
        agents = db.query(Agent).filter(Agent.is_active == True).all()
        return [
            {
                "id": agent.id,
                "name": agent.name,
                "description": agent.description
            }
            for agent in agents
        ]
    
    @staticmethod
    def get_available_mcps(db: Session) -> List[Dict[str, Any]]:
        """获取可用的MCP列表"""
        mcps = db.query(MCP).all()
        return [
            {
                "id": mcp.id,
                "name": mcp.name,
                "provider": mcp.provider,
                "model": mcp.model
            }
            for mcp in mcps
        ]
    
    @staticmethod
    def _convert_to_response(db_ai_app: AIApp) -> AIAppResponse:
        """将数据库模型转换为响应Schema"""
        # 解析JSON字段
        agent_list = None
        if db_ai_app.agent_list:
            try:
                agent_data = json.loads(db_ai_app.agent_list)
                agent_list = [AgentConfig(**agent) for agent in agent_data]
            except:
                pass
        
        mcp_list = None
        if db_ai_app.mcp_list:
            try:
                mcp_data = json.loads(db_ai_app.mcp_list)
                mcp_list = [MCPConfig(**mcp) for mcp in mcp_data]
            except:
                pass
        
        llm_config = None
        if db_ai_app.llm_config:
            try:
                llm_data = json.loads(db_ai_app.llm_config)
                llm_config = [LLMConfig(**llm) for llm in llm_data]
            except:
                pass
        
        return AIAppResponse(
            id=db_ai_app.id,
            name=db_ai_app.name,
            identifier=db_ai_app.identifier,
            icon=db_ai_app.icon,
            description=db_ai_app.description,
            is_active=db_ai_app.is_active,
            dashboard_url=db_ai_app.dashboard_url,
            access_url=db_ai_app.access_url,
            main_agent_id=db_ai_app.main_agent_id,
            agent_list=agent_list,
            mcp_list=mcp_list,
            llm_config=llm_config,
            system_prompt=db_ai_app.system_prompt,
            app_type=db_ai_app.app_type,
            user_id=db_ai_app.user_id,
            created_at=db_ai_app.created_at,
            updated_at=db_ai_app.updated_at
        ) 