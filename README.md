# 项目管理工具
```sh
# 初始化项目
uv init ai-agent-python

# 安装依赖
uv sync

# 安装依赖
uv run uvicorn app.main:app --reload
```

## 项目结构

```text
app/
├── api/              FastAPI 接口层
├── core/             核心配置、常量、日志、异常
├── schemas/          Pydantic 请求与响应模型
├── services/         业务逻辑层
├── repositories/     数据访问层
├── models/           数据库 ORM 模型
└── dependencies/     FastAPI 依赖注入

## api文档：http://127.0.0.1:8000/docs