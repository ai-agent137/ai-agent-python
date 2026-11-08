from fastapi import FastAPI, Query
from app.api.v1.chat import router as chat_router

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0",
)

app.include_router(chat_router, prefix="/v1/api", tags=["Chat API"])
chat_router
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/search")
async def search(
    q: str = Query(..., description="Search query string"),
    page: int = Query(1, ge=1, le=100, description="Page number for pagination")
):
    return {"query": q, "page": page}