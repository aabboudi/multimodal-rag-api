from fastapi import FastAPI
from .api.v1.api_v1 import router as api_v1_router

app = FastAPI(
  title="RAG API for LLaMa3 via Ollama",
  description="This API allows you to do amazing things!",
  version="0.1.0",
)

app.include_router(api_v1_router, prefix="/api/v1")
