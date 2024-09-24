import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import CSVLoader

def load_docs(format, data_path):
  load_functions = {
    "pdf": load_pdf_docs,
    "csv": load_csv_docs,
  }

  load_function = load_functions.get(format, lambda: "Unsupported file extension")
  return load_function(data_path)

# TODO: PyPDFDirectoryLoader is deprecated
def load_pdf_docs(data_path):
  laoder = PyPDFDirectoryLoader(data_path)
  pdf_documents = laoder.load()
  print(f"Loaded {len(pdf_documents)} PDF documents.")
  return pdf_documents

def load_csv_docs(data_path):
  csv_documents = []
  for file_name in os.listdir(data_path):
    if file_name.endswith(".csv"):
      file_path = os.path.join(data_path, file_name)
      loader = CSVLoader(file_path=file_path, encoding="utf-8")
      csv_documents.extend(loader.load())
  print(f"Loaded {len(csv_documents)} CSV documents.")
  return csv_documents
