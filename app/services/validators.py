from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB
ALLOWED_EXT = {"pdf", "csv", "md"}

def validate_file_ext(file_name: str):
  ext = file_name.split('.')[-1].lower()
  if ext not in ALLOWED_EXT:
    raise HTTPException(
      status_code=400,
      detail=f"File extension '{ext}' is not allowed"
    )
  else:
    return ext

def validate_file_size(file: UploadFile):
  file_size = len(file.file.read())
  file.file.seek(0)
  if file_size > MAX_FILE_SIZE:
    raise HTTPException(
      status_code=400,
      detail=f"File size exceeds the maximum of {MAX_FILE_SIZE // (1024 * 1024)} MB"
    )
