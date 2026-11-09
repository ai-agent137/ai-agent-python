# ai应用
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
```

## api文档：http://127.0.0.1:8000/docs

## 错误响应格式
{
  "code": 50000,
  "message": "服务器内部错误",
  "data": null,
  "trace_id": "trace_xxx"
}


##  当前完整请求链路

```text id="ye5h2t"
HTTP Request
    ↓
trace_and_log_middleware
    ↓
生成 trace_id
    ↓
记录 request_start
    ↓
verify_api_key
    ↓
get_current_user
    ↓
Router
    ↓
Service
    ↓
Repository / LLM / RAG
    ↓
如果成功：ApiResponse
    ↓
如果失败：Exception Handler -> ErrorResponse
    ↓
Middleware 添加响应头
    ↓
记录 request_end
    ↓
HTTP Response