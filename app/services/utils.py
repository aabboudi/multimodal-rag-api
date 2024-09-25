import unicodedata

def is_valid(char: str) -> bool:
  if unicodedata.category(char).startswith(('L', 'N')):
    return True
  if char in '_.-':
    return True
  return False

def sanitize_string(string: str) -> str:
  return ''.join(char if is_valid(char) else '_' for char in string)
