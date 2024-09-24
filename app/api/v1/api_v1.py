from fastapi import APIRouter, UploadFile, File
from datetime import datetime, timezone
from langchain_community.embeddings.ollama import OllamaEmbeddings

from app.rag.load import load_docs
from app.rag.embed import embed_docs
from app.rag.query import query_rag
from app.services.utils import sanitize_string
from app.services.validators import *
from app.config import EMBEDDING_MODEL

# embeddings = OllamaEmbeddings(model="nomic-embed-text")
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

router = APIRouter()

@router.get("/")
def health_check():
  return {"Status": "Running"}


# TODO: Add filter to store files with the same format in a single directory
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
  format = validate_file_ext(file.filename)
  validate_file_size(file)

  now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
  clean_filename = sanitize_string(file.filename)
  file_location = f"data/{format}/{now}_{clean_filename}"

  with open(file_location, "wb+") as file_object:
    file_object.write(file.file.read())

  docs = load_docs(format, f"data/{format}")
  embed_docs(docs)

  return {
    "file_name": clean_filename,
    "file_format": format,
    "embedding": "started"
  }


@router.post("/ask")
def ask_embedded_files(query: str):
  query = query
  response = query_rag(query, "chroma", embeddings)
  return {
    "query": query,
    "response": response,
  }
