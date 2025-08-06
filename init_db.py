#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建MySQL数据库和表结构
"""

from app.config import settings
from app.db.session import init_db, engine
from app.models.mcp import Base

def create_tables():
    """创建表结构"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("表结构创建成功")
        return True
    except Exception as e:
        print(f"创建表结构失败: {e}")
        return False

def main():
    """主函数"""
    print("开始初始化数据库...")
    
    # 创建表结构
    if create_tables():
        print("表结构创建完成")
    else:
        print("表结构创建失败")
        return
    
    print("数据库初始化完成！")

if __name__ == "__main__":
    main() 