from fastapi import APIRouter, File, UploadFile
from datetime import datetime

from app.services.validators import *
from app.services.utils import sanitize_string

router = APIRouter()

@router.get("/")
def health_check():
  return {"Status": "Running"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
  validate_file_ext(file.filename)
  validate_file_size(file)

  now = datetime.now().isoformat(timespec="seconds").replace("-", "").replace(":", "")
  clean_filename = sanitize_string(file.filename)
  file_location = f"data/{now + "_" + clean_filename}"

  with open(file_location, "wb+") as file_object:
    file_object.write(file.file.read())

  return {"filename": clean_filename}
