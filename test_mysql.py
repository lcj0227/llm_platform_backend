#!/usr/bin/env python3
"""
MySQL数据库测试脚本
测试数据库连接和API功能
"""

import requests
import json
import time
from sqlalchemy import text

# API基础URL
BASE_URL = "http://localhost:8000"

def test_database_connection():
    """测试数据库连接"""
    print("=== 测试数据库连接 ===")
    try:
        from app.db.session import engine, SessionLocal
        from app.models.mcp import MCP
        
        # 测试连接
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
        
        # 测试查询
        db = SessionLocal()
        try:
            count = db.query(MCP).count()
            print(f"✅ 查询成功，当前MCP记录数: {count}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    
    return True

def test_create_mcp():
    """测试创建MCP"""
    print("\n=== 测试创建MCP ===")
    
    mcp_data = {
        "id": "test-mcp-002",
        "name": "测试MCP",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "temperature": "0.7",
        "api_key": "sk-test-key-123456",
        "tool_plugins": ["tool3", "tool4"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mcp/", json=mcp_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 创建MCP成功: {result['name']}")
            return result['id']
        else:
            print(f"❌ 创建MCP失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 创建MCP异常: {e}")
        return None

def test_list_mcps():
    """测试获取MCP列表"""
    print("\n=== 测试获取MCP列表 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/mcp/")
        if response.status_code == 200:
            mcps = response.json()
            print(f"✅ 获取MCP列表成功，共 {len(mcps)} 条记录")
            for mcp in mcps:
                print(f"  - {mcp['name']} ({mcp['provider']})")
            return mcps
        else:
            print(f"❌ 获取MCP列表失败: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ 获取MCP列表异常: {e}")
        return []

def test_update_mcp(mcp_id):
    """测试更新MCP"""
    print(f"\n=== 测试更新MCP {mcp_id} ===")
    
    update_data = {
        "name": "更新后的测试MCP",
        "temperature": "0.8",
        "tool_plugins": ["tool1", "tool2", "tool3"]
    }
    
    try:
        response = requests.put(f"{BASE_URL}/mcp/{mcp_id}", json=update_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 更新MCP成功: {result['name']}")
            return True
        else:
            print(f"❌ 更新MCP失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 更新MCP异常: {e}")
        return False

def test_delete_mcp(mcp_id):
    """测试删除MCP"""
    print(f"\n=== 测试删除MCP {mcp_id} ===")
    
    try:
        response = requests.delete(f"{BASE_URL}/mcp/{mcp_id}")
        if response.status_code == 200:
            print(f"✅ 删除MCP成功")
            return True
        else:
            print(f"❌ 删除MCP失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 删除MCP异常: {e}")
        return False

def main():
    """主测试函数"""
    print("开始MySQL数据库测试...")
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 测试数据库连接
    if not test_database_connection():
        print("数据库连接测试失败，退出测试")
        return
    
    # 测试创建MCP
    mcp_id = test_create_mcp()
    if not mcp_id:
        print("创建MCP测试失败，跳过后续测试")
        return
    
    # 测试获取MCP列表
    test_list_mcps()
    
    # 测试更新MCP
    test_update_mcp(mcp_id)
    
    # 再次获取列表查看更新结果
    test_list_mcps()
    
    # 测试删除MCP
    test_delete_mcp(mcp_id)
    
    # 最终获取列表确认删除
    test_list_mcps()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main() 