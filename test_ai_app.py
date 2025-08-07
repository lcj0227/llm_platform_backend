#!/usr/bin/env python3
"""
AI应用管理功能测试脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_ai_app():
    """测试创建AI应用"""
    print("=== 测试创建AI应用 ===")
    
    # 创建AI应用数据（简化版本）
    ai_app_data = {
        "name": "智能客服助手",
        "identifier": "smart-customer-service",
        "icon": "https://example.com/icon.png",
        "description": "一个智能客服助手，能够回答用户问题并提供帮助",
        "is_active": True,
        "dashboard_url": "https://dashboard.example.com",
        "main_agent_id": None,  # 使用默认Agent
        "agent_list": None,  # 暂时不设置复杂结构
        "mcp_list": None,  # 暂时不设置复杂结构
        "llm_config": None,  # 暂时不设置复杂结构
        "system_prompt": "你是一个智能客服助手，请根据用户的问题提供准确、有用的回答。",
        "app_type": "platform",
        "user_id": None
    }
    
    response = requests.post(f"{BASE_URL}/ai-apps/", json=ai_app_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 创建AI应用成功")
        print(f"应用ID: {result['id']}")
        print(f"访问URL: {result['access_url']}")
        return result['id']
    else:
        print("❌ 创建AI应用失败")
        return None

def test_get_ai_apps():
    """测试获取AI应用列表"""
    print("=== 测试获取AI应用列表 ===")
    
    response = requests.get(f"{BASE_URL}/ai-apps/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 获取AI应用列表成功")
        print(f"总数: {result['total']}")
        print(f"当前页: {result['page']}")
        print(f"每页数量: {result['size']}")
        print(f"应用数量: {len(result['apps'])}")
        
        for app in result['apps']:
            print(f"- {app['name']} ({app['identifier']})")
    else:
        print("❌ 获取AI应用列表失败")

def test_get_ai_app(app_id: str):
    """测试获取单个AI应用"""
    print(f"=== 测试获取单个AI应用 (ID: {app_id}) ===")
    
    response = requests.get(f"{BASE_URL}/ai-apps/{app_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 获取AI应用详情成功")
        print(f"应用名称: {result['name']}")
        print(f"应用标识: {result['identifier']}")
        print(f"启用状态: {result['is_active']}")
        print(f"访问URL: {result['access_url']}")
        print(f"Agent数量: {len(result['agent_list']) if result['agent_list'] else 0}")
        print(f"MCP数量: {len(result['mcp_list']) if result['mcp_list'] else 0}")
    else:
        print("❌ 获取AI应用详情失败")

def test_update_ai_app(app_id: str):
    """测试更新AI应用"""
    print(f"=== 测试更新AI应用 (ID: {app_id}) ===")
    
    update_data = {
        "description": "更新后的智能客服助手描述",
        "is_active": True,
        "system_prompt": "更新后的系统提示词：你是一个专业的智能客服助手，请提供准确、友好的服务。"
    }
    
    response = requests.put(f"{BASE_URL}/ai-apps/{app_id}", json=update_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 更新AI应用成功")
        print(f"更新后的描述: {result['description']}")
        print(f"更新后的系统提示词: {result['system_prompt']}")
    else:
        print("❌ 更新AI应用失败")

def test_generate_system_prompt():
    """测试自动生成系统提示词"""
    print("=== 测试自动生成系统提示词 ===")
    
    request_data = {
        "app_name": "数据分析助手",
        "app_description": "一个专门用于数据分析的AI助手",
        "agent_list": None,  # 简化测试
        "mcp_list": None  # 简化测试
    }
    
    response = requests.post(f"{BASE_URL}/ai-apps/generate-system-prompt", json=request_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 生成系统提示词成功")
        print("生成的系统提示词:")
        print(result['system_prompt'])
    else:
        print("❌ 生成系统提示词失败")

def test_get_available_resources():
    """测试获取可用资源"""
    print("=== 测试获取可用资源 ===")
    
    # 获取可用Agent
    print("--- 获取可用Agent ---")
    response = requests.get(f"{BASE_URL}/ai-apps/available/agents")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 获取可用Agent成功")
        print(f"Agent数量: {len(result['agents'])}")
        for agent in result['agents']:
            print(f"- {agent['name']} ({agent['id']})")
    else:
        print("❌ 获取可用Agent失败")
    
    # 获取可用MCP
    print("--- 获取可用MCP ---")
    response = requests.get(f"{BASE_URL}/ai-apps/available/mcps")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 获取可用MCP成功")
        print(f"MCP数量: {len(result['mcps'])}")
        for mcp in result['mcps']:
            print(f"- {mcp['name']} ({mcp['id']})")
    else:
        print("❌ 获取可用MCP失败")

def test_delete_ai_app(app_id: str):
    """测试删除AI应用"""
    print(f"=== 测试删除AI应用 (ID: {app_id}) ===")
    
    response = requests.delete(f"{BASE_URL}/ai-apps/{app_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 删除AI应用成功")
        print(result['message'])
    else:
        print("❌ 删除AI应用失败")

def test_create_user_app():
    """测试创建用户应用"""
    print("=== 测试创建用户应用 ===")
    
    user_app_data = {
        "name": "个人助手",
        "identifier": "personal-assistant",
        "description": "我的个人AI助手",
        "is_active": True,
        "app_type": "user",
        "user_id": "user-123"
    }
    
    response = requests.post(f"{BASE_URL}/ai-apps/", json=user_app_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 创建用户应用成功")
        print(f"应用ID: {result['id']}")
        print(f"应用类型: {result['app_type']}")
        print(f"用户ID: {result['user_id']}")
        return result['id']
    else:
        print("❌ 创建用户应用失败")
        return None

def main():
    """主测试函数"""
    print("开始测试AI应用管理功能...")
    print()
    
    try:
        # 测试创建AI应用
        app_id = test_create_ai_app()
        
        if app_id:
            # 测试获取AI应用列表
            test_get_ai_apps()
            
            # 测试获取单个AI应用
            test_get_ai_app(app_id)
            
            # 测试更新AI应用
            test_update_ai_app(app_id)
            
            # 测试自动生成系统提示词
            test_generate_system_prompt()
            
            # 测试获取可用资源
            test_get_available_resources()
            
            # 测试创建用户应用
            user_app_id = test_create_user_app()
            
            # 测试删除AI应用
            test_delete_ai_app(app_id)
            
            if user_app_id:
                test_delete_ai_app(user_app_id)
        
        print("测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    main() 