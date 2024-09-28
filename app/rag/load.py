from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, CSVLoader, UnstructuredMarkdownLoader

def get_loader_cls(data_format):
  match data_format:
    case "pdf": return PyPDFLoader
    case "csv": return CSVLoader
    case "md": return UnstructuredMarkdownLoader
    case _: return 0

def load_dir(data_path, data_format):
  loader_cls = get_loader_cls(data_format)
  if not loader_cls:
    return None

  loader = DirectoryLoader(data_path, glob=f"**/*.{data_format}", loader_cls=loader_cls)
  docs = loader.load()
  print(f"Loaded {len(docs)} documents of type {data_format}.")
  return docs

def load_file(file_path, file_format):
  loader_cls = get_loader_cls(file_format)
  loader = loader_cls(file_path)
  file = loader.load()
  print(f"Loaded {len(file)} document of type {file_format}.")
  return file
