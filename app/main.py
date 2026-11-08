from fastapi import FastAPI, Query
from app.api.v1.chat import router as chat_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.rag import router as rag_router
from app.api.v1.health import router as health_router
app = FastAPI(
    title="AI Agent  API Application",
    description="Python + FastAPI + LLM + Agent",
    version="1.0.0",
)

app.include_router(chat_router, prefix="/v1/api", tags=["Chat API"])
app.include_router(conversations_router, prefix="/api/v1", tags=["Conversations"])
app.include_router(rag_router, prefix="/api/v1", tags=["RAG API"])
app.include_router(health_router, prefix="/api/v1", tags=["Health API"])

@app.get("/")
async def root():
    return {
        "message": "AI Agent Course API"
    }