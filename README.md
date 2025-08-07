# LLM平台后端 - MySQL版本

这是一个基于FastAPI和MySQL的LLM平台后端服务。

## 功能特性

- 基于FastAPI的RESTful API
- MySQL数据库支持
- MCP (Model Context Protocol) 管理
- Agent管理
- **AI应用管理** - 支持平台应用和用户应用的管理
- 支持多种LLM提供商配置

## 系统要求

- Python 3.8+
- MySQL 5.7+ 或 MySQL 8.0+
- pip

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd llm_platform_backend
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置MySQL

确保MySQL服务正在运行，并创建数据库用户：

```sql
-- 登录MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE llm_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER 'llm_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON llm_platform.* TO 'llm_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. 配置环境变量

创建 `.env` 文件：

```env
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=llm_platform
```

### 5. 初始化数据库

```bash
python init_db.py
```

### 6. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### MCP管理

- `POST /mcp/` - 创建新的MCP配置
- `GET /mcp/` - 获取所有MCP配置
- `PUT /mcp/{mcp_id}` - 更新MCP配置
- `DELETE /mcp/{mcp_id}` - 删除MCP配置

### Agent管理

- `POST /agent/` - 创建新的Agent配置
- `GET /agent/` - 获取所有Agent配置
- `GET /agent/{agent_id}` - 获取单个Agent配置
- `PUT /agent/{agent_id}` - 更新Agent配置
- `DELETE /agent/{agent_id}` - 删除Agent配置
- `GET /agent/mcp/{mcp_id}` - 根据MCP获取Agent列表

### AI应用管理

#### 基础CRUD操作
- `POST /ai-apps/` - 创建AI应用
- `GET /ai-apps/` - 获取AI应用列表
- `GET /ai-apps/{app_id}` - 获取单个AI应用
- `PUT /ai-apps/{app_id}` - 更新AI应用
- `DELETE /ai-apps/{app_id}` - 删除AI应用

#### 特殊功能
- `POST /ai-apps/generate-system-prompt` - 自动生成系统提示词
- `GET /ai-apps/available/agents` - 获取可用Agent列表
- `GET /ai-apps/available/mcps` - 获取可用MCP列表
- `GET /ai-apps/platform` - 获取平台应用列表
- `GET /ai-apps/user/{user_id}` - 获取用户应用列表

## 功能详解

### AI应用管理

AI应用管理支持创建和管理两类AI应用：

#### 1. 基础配置
- **应用名称**：应用的显示名称
- **应用标识符**：唯一标识符，用于生成独立访问URL
- **图标**：应用图标URL
- **描述**：应用详细描述
- **启用状态**：控制应用是否可用
- **默认Dashboard地址**：配置的Dashboard URL
- **独立访问URL**：根据标识符自动生成的可独立访问的URL

#### 2. Agent配置
- **主Agent配置**：负责Agent间调度和事务处理的主Agent
  - 可选择现有Agent或使用内置默认Agent
- **Agent列表配置**：可选择多个Agent用于应用

#### 3. MCP配置
- 可从MCP列表选择多个MCP
- 支持MCP名称、描述显示
- 支持添加自定义优化描述

#### 4. 系统配置
- **大模型配置**：支持选择多个大模型
- **系统提示词**：应用的系统提示词
- **自动生成**：支持根据应用信息自动生成系统提示词（仅当主Agent选择默认Agent时可用）

#### 应用类型
- **平台应用**：由平台管理员创建的应用
- **我的应用**：由用户个人创建的应用

## 测试

运行测试脚本：

```bash
python test_mysql.py
python test_agent.py
python test_ai_app.py
```

## 数据库结构

### MCP表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(255) | 主键，MCP唯一标识 |
| name | VARCHAR(255) | MCP名称 |
| provider | VARCHAR(100) | 提供商（openai, azure等） |
| model | VARCHAR(100) | 模型名称（gpt-3.5-turbo等） |
| temperature | VARCHAR(10) | 温度参数 |
| api_key | TEXT | API密钥 |
| tool_plugins | TEXT | 工具插件（JSON格式） |

### Agent表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(255) | 主键，Agent唯一标识 |
| name | VARCHAR(255) | Agent名称 |
| description | TEXT | Agent描述 |
| system_prompt | TEXT | 系统提示词 |
| temperature | VARCHAR(10) | 温度参数 |
| max_tokens | VARCHAR(10) | 最大token数 |
| is_active | BOOLEAN | 是否激活 |
| mcp_id | VARCHAR(255) | 关联的MCP ID |
| tools | TEXT | 工具配置（JSON格式） |

### AI应用表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(255) | 主键ID |
| name | VARCHAR(255) | 应用名称 |
| identifier | VARCHAR(255) | 应用标识符（唯一） |
| icon | VARCHAR(500) | 应用图标URL |
| description | TEXT | 应用描述 |
| is_active | BOOLEAN | 启用状态 |
| dashboard_url | VARCHAR(500) | 默认Dashboard地址 |
| access_url | VARCHAR(500) | 独立访问URL |
| main_agent_id | VARCHAR(255) | 主Agent ID |
| agent_list | TEXT | Agent列表（JSON格式） |
| mcp_list | TEXT | MCP列表（JSON格式） |
| llm_config | TEXT | 大模型配置（JSON格式） |
| system_prompt | TEXT | 系统提示词 |
| app_type | VARCHAR(50) | 应用类型 |
| user_id | VARCHAR(255) | 创建用户ID |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 使用示例

### 创建AI应用

```python
import requests

# 创建平台应用
app_data = {
    "name": "智能客服助手",
    "identifier": "smart-customer-service",
    "description": "一个智能客服助手，能够回答用户问题并提供帮助",
    "is_active": True,
    "app_type": "platform",
    "user_id": None
}

response = requests.post("http://localhost:8000/ai-apps/", json=app_data)
app = response.json()
print(f"创建的应用ID: {app['id']}")
print(f"访问URL: {app['access_url']}")
```

### 自动生成系统提示词

```python
# 生成系统提示词
prompt_request = {
    "app_name": "数据分析助手",
    "app_description": "一个专门用于数据分析的AI助手",
    "agent_list": [
        {
            "agent_id": "agent-001",
            "name": "数据分析Agent",
            "description": "专门处理数据分析任务"
        }
    ]
}

response = requests.post("http://localhost:8000/ai-apps/generate-system-prompt", 
                        json=prompt_request)
result = response.json()
print(f"生成的系统提示词: {result['system_prompt']}")
```

## 开发

### 项目结构

```
app/
├── api/           # API路由
│   ├── mcp.py     # MCP管理API
│   ├── agent.py   # Agent管理API
│   └── ai_app.py  # AI应用管理API
├── db/           # 数据库配置
├── models/       # 数据模型
│   ├── mcp.py    # MCP模型
│   ├── agent.py  # Agent模型
│   └── ai_app.py # AI应用模型
├── schemas/      # Pydantic模式
│   ├── mcp.py    # MCP模式
│   ├── agent.py  # Agent模式
│   └── ai_app.py # AI应用模式
├── services/     # 业务逻辑
│   └── ai_app.py # AI应用服务
└── main.py       # 应用入口

config.py         # 配置文件
init_db.py        # 数据库初始化脚本
test_mysql.py     # 测试脚本
test_agent.py     # Agent测试脚本
test_ai_app.py    # AI应用测试脚本
requirements.txt   # 依赖包
```

### 添加新功能

1. 在 `app/models/` 中定义数据模型
2. 在 `app/schemas/` 中定义API模式
3. 在 `app/services/` 中实现业务逻辑
4. 在 `app/api/` 中定义API路由

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否运行
   - 验证数据库连接参数
   - 确保数据库用户有足够权限

2. **表创建失败**
   - 检查数据库是否存在
   - 验证字符集设置
   - 查看错误日志

3. **API请求失败**
   - 检查服务是否正常启动
   - 验证请求格式
   - 查看服务器日志

4. **Python客户端连接问题**
   - 如果使用Anaconda环境，可能存在代理问题
   - 尝试使用系统Python或配置代理设置
   - 使用curl等工具验证API是否正常工作

## 许可证

MIT License 