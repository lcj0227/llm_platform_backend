#!/usr/bin/env python3
"""
Agent功能测试脚本
用于测试Agent的CRUD操作
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_agent():
    """测试创建Agent"""
    print("=== 测试创建Agent ===")
    
    agent_data = {
        "id": "agent_004",
        "name": "智能助手4",
        "description": "第四个智能助手",
        "system_prompt": "你是一个有用的AI助手，可以帮助用户解决各种问题。",
        "temperature": "0.7",
        "max_tokens": "4000",
        "is_active": True,
        "mcp_id": "test-001",  # 使用数据库中实际存在的MCP ID
        "tools": [
            {
                "name": "web_search",
                "description": "搜索网络信息",
                "enabled": True
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/agent/", json=agent_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

def test_list_agents():
    """测试获取Agent列表"""
    print("=== 测试获取Agent列表 ===")
    
    response = requests.get(f"{BASE_URL}/agent/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

def test_get_agent():
    """测试获取单个Agent"""
    print("=== 测试获取单个Agent ===")
    
    agent_id = "agent_004"
    response = requests.get(f"{BASE_URL}/agent/{agent_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

def test_update_agent():
    """测试更新Agent"""
    print("=== 测试更新Agent ===")
    
    agent_id = "agent_004"
    update_data = {
        "name": "更新后的智能助手4",
        "description": "更新后的描述",
        "system_prompt": "你是一个有用的AI助手，可以帮助用户解决各种问题。",
        "temperature": "0.8",
        "max_tokens": "4000",
        "is_active": True,
        "mcp_id": "test-001",
        "tools": [
            {
                "name": "web_search",
                "description": "搜索网络信息",
                "enabled": True
            }
        ]
    }
    
    response = requests.put(f"{BASE_URL}/agent/{agent_id}", json=update_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

def test_get_agents_by_mcp():
    """测试根据MCP获取Agent列表"""
    print("=== 测试根据MCP获取Agent列表 ===")
    
    mcp_id = "test-001"
    response = requests.get(f"{BASE_URL}/agent/mcp/{mcp_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

def test_delete_agent():
    """测试删除Agent"""
    print("=== 测试删除Agent ===")
    
    agent_id = "agent_004"
    response = requests.delete(f"{BASE_URL}/agent/{agent_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

def main():
    """主函数"""
    print("开始测试Agent功能...")
    print()
    
    try:
        test_create_agent()
        test_list_agents()
        test_get_agent()
        test_update_agent()
        test_get_agents_by_mcp()
        test_delete_agent()
        
        print("测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    main() 