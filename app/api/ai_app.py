from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.services.ai_app import AIAppService
from app.schemas.ai_app import (
    AIAppCreate,
    AIAppUpdate,
    AIAppResponse,
    AIAppListResponse,
    GenerateSystemPromptRequest
)

router = APIRouter(prefix="/ai-apps", tags=["AI应用管理"])

@router.post("/", response_model=AIAppResponse, summary="创建AI应用")
async def create_ai_app(
    ai_app_data: AIAppCreate,
    db: Session = Depends(get_db)
):
    """
    创建新的AI应用
    
    - **name**: 应用名称
    - **identifier**: 应用标识符（唯一）
    - **icon**: 应用图标URL（可选）
    - **description**: 应用描述（可选）
    - **is_active**: 启用状态
    - **dashboard_url**: 默认Dashboard地址（可选）
    - **main_agent_id**: 主Agent ID（可选，null表示使用默认Agent）
    - **agent_list**: Agent列表（可选）
    - **mcp_list**: MCP列表（可选）
    - **llm_config**: 大模型配置（可选）
    - **system_prompt**: 系统提示词（可选）
    - **app_type**: 应用类型（platform-平台应用，user-我的应用）
    - **user_id**: 创建用户ID（可选）
    """
    try:
        return AIAppService.create_ai_app(db, ai_app_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建AI应用失败: {str(e)}")

@router.get("/", response_model=AIAppListResponse, summary="获取AI应用列表")
async def get_ai_apps(
    app_type: Optional[str] = Query(None, description="应用类型：platform-平台应用，user-我的应用"),
    user_id: Optional[str] = Query(None, description="用户ID"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取AI应用列表
    
    - **app_type**: 应用类型过滤
    - **user_id**: 用户ID过滤
    - **page**: 页码
    - **size**: 每页数量
    """
    skip = (page - 1) * size
    result = AIAppService.get_ai_apps(db, app_type, user_id, skip, size)
    return AIAppListResponse(**result)

@router.get("/{app_id}", response_model=AIAppResponse, summary="获取单个AI应用")
async def get_ai_app(
    app_id: str,
    db: Session = Depends(get_db)
):
    """
    根据ID获取单个AI应用详情
    """
    ai_app = AIAppService.get_ai_app(db, app_id)
    if not ai_app:
        raise HTTPException(status_code=404, detail="AI应用不存在")
    return ai_app

@router.put("/{app_id}", response_model=AIAppResponse, summary="更新AI应用")
async def update_ai_app(
    app_id: str,
    ai_app_data: AIAppUpdate,
    db: Session = Depends(get_db)
):
    """
    更新AI应用信息
    
    可以更新以下字段：
    - **name**: 应用名称
    - **identifier**: 应用标识符
    - **icon**: 应用图标URL
    - **description**: 应用描述
    - **is_active**: 启用状态
    - **dashboard_url**: 默认Dashboard地址
    - **main_agent_id**: 主Agent ID
    - **agent_list**: Agent列表
    - **mcp_list**: MCP列表
    - **llm_config**: 大模型配置
    - **system_prompt**: 系统提示词
    """
    ai_app = AIAppService.update_ai_app(db, app_id, ai_app_data)
    if not ai_app:
        raise HTTPException(status_code=404, detail="AI应用不存在")
    return ai_app

@router.delete("/{app_id}", summary="删除AI应用")
async def delete_ai_app(
    app_id: str,
    db: Session = Depends(get_db)
):
    """
    删除AI应用
    """
    success = AIAppService.delete_ai_app(db, app_id)
    if not success:
        raise HTTPException(status_code=404, detail="AI应用不存在")
    return {"message": "AI应用删除成功"}

@router.post("/generate-system-prompt", summary="自动生成系统提示词")
async def generate_system_prompt(
    request: GenerateSystemPromptRequest
):
    """
    根据应用信息自动生成系统提示词
    
    - **app_name**: 应用名称
    - **app_description**: 应用描述（可选）
    - **agent_list**: Agent列表（可选）
    - **mcp_list**: MCP列表（可选）
    """
    try:
        system_prompt = AIAppService.generate_system_prompt(request)
        return {"system_prompt": system_prompt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"生成系统提示词失败: {str(e)}")

@router.get("/available/agents", summary="获取可用的Agent列表")
async def get_available_agents(
    db: Session = Depends(get_db)
):
    """
    获取可用的Agent列表，用于AI应用配置时选择
    """
    agents = AIAppService.get_available_agents(db)
    return {"agents": agents}

@router.get("/available/mcps", summary="获取可用的MCP列表")
async def get_available_mcps(
    db: Session = Depends(get_db)
):
    """
    获取可用的MCP列表，用于AI应用配置时选择
    """
    mcps = AIAppService.get_available_mcps(db)
    return {"mcps": mcps}

@router.get("/platform", response_model=AIAppListResponse, summary="获取平台应用列表")
async def get_platform_apps(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取平台应用列表
    """
    skip = (page - 1) * size
    result = AIAppService.get_ai_apps(db, app_type="platform", skip=skip, limit=size)
    return AIAppListResponse(**result)

@router.get("/user/{user_id}", response_model=AIAppListResponse, summary="获取用户应用列表")
async def get_user_apps(
    user_id: str,
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取指定用户的应用列表
    """
    skip = (page - 1) * size
    result = AIAppService.get_ai_apps(db, user_id=user_id, skip=skip, limit=size)
    return AIAppListResponse(**result) 