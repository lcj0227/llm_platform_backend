# LLM平台后端 - MySQL版本

这是一个基于FastAPI和MySQL的LLM平台后端服务。

## 功能特性

- 基于FastAPI的RESTful API
- MySQL数据库支持
- MCP (Model Context Protocol) 管理
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

## 测试

运行测试脚本：

```bash
python test_mysql.py
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

## 开发

### 项目结构

```
app/
├── api/           # API路由
├── db/           # 数据库配置
├── models/       # 数据模型
├── schemas/      # Pydantic模式
├── services/     # 业务逻辑
└── main.py       # 应用入口

config.py         # 配置文件
init_db.py        # 数据库初始化脚本
test_mysql.py     # 测试脚本
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

## 许可证

MIT License 