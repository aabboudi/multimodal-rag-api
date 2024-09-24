import re

def sanitize_string(string: str) -> str:
  return re.sub(r'[^a-zA-Z0-9_.-]', '_', string)
