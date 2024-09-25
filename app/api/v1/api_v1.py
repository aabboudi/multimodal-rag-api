from fastapi import APIRouter, UploadFile, File
from datetime import datetime, timezone
from langchain_community.embeddings.ollama import OllamaEmbeddings

from app.rag.load import load_file
from app.rag.embed import embed_docs
from app.rag.query import query_rag
from app.services.utils import sanitize_string
from app.services.validators import *
from app.config import EMBEDDING_MODEL

router = APIRouter()

@router.get("/")
def health_check():
  return {"Status": "Running"}


# TODO: Add filter to store files with the same format in a single directory
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
  file_format = validate_file_ext(file.filename)
  validate_file_size(file)

  now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
  clean_filename = sanitize_string(file.filename)
  file_location = f"data/{file_format}/{now}_{clean_filename}"

  with open(file_location, "wb+") as file_object:
    file_object.write(file.file.read())

  file = load_file(file_location, file_format)
  embed_docs(file)

  return {
    "filename": clean_filename,
    "file_format": file_format,
    "embedding_status": "started",
  }


@router.post("/ask")
def ask_embedded_files(query: str):
  query = query
  embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
  response = query_rag(query, "chroma", embeddings)
  return {
    "query": query,
    "response": response,
  }
