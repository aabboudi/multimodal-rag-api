from fastapi import FastAPI
from .api.api_v1 import router as api_v1_router

app = FastAPI(
  title="Multimodal RAG API",
  description="Document-based retrieval-augmented generation system for large language models",
  version="0.1.0",
)

app.include_router(api_v1_router, prefix="/api/v1")
