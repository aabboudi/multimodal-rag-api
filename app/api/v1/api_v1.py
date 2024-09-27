import os
import shutil
from fastapi import APIRouter, UploadFile, File
from datetime import datetime, timezone
from langchain_chroma import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings

from app.rag.load import load_file
from app.rag.embed import embed_docs
from app.rag.query import query_rag
from app.services.utils import sanitize_string
from app.services.validators import *
from app.config import EMBEDDING_MODEL, CHROMA_PATH

router = APIRouter()

@router.get("/")
def health_check():
  return {"Status": "Running"}


@router.get("/database-count")
def count_vector_elements():
  embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
  DB = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
  db_count = len(DB.get(include=[]))
  return {"number_of_docs": db_count}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
  file_format = validate_file_ext(file.filename)
  validate_file_size(file)

  now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
  clean_filename = f"{now}_{sanitize_string(file.filename)}"

  directory = f"data/{file_format}"
  os.makedirs(directory, exist_ok=True)
  file_location = f"{directory}/{clean_filename}"

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


@router.post("/reset")
def clear_database(confirm: bool):
  if confirm:
    if os.path.exists(CHROMA_PATH):
      shutil.rmtree(CHROMA_PATH)
      print(f"Database at {CHROMA_PATH} has been cleared.")
      return {"status": "database cleared"}
    else:
      print("Could not clear database. Directory not found")
      raise HTTPException(
        status_code=400,
        detail="no database found"
      )
  else:
    print("Operation not allowed")
    raise HTTPException(
      status_code=403,
      detail="operation not allowed"
    )
