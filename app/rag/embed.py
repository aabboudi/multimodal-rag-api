from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.config import CHROMA_PATH, DATA_PATH, EMBEDDING_MODEL

def embed_docs(docs):
  embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
  db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

  chunks = split_docs(docs)
  chunks_with_ids = calculate_chunk_ids(chunks)
  existing_items = db.get(include=[])
  existing_ids = set(existing_items["ids"])

  print(f"Number of existing documents in DB: {len(existing_ids)}")

  new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

  if new_chunks:
    print(f"👉 Adding new documents: {len(new_chunks)}")
    new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    db.add_documents(new_chunks, ids=new_chunk_ids)
    # db.persist()
    print(f"✅ Successfully added {len(new_chunks)} new documents.")
  else:
    print("✅ No new documents to add")


# Split docs into chunks
def split_docs(docs, CHUNK_SIZE=800, CHUNK_OVERLAP=80):
  chunks = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    is_separator_regex=False
  ).split_documents(docs)

  print(f"Split documents into {len(chunks)} chunks.")
  return chunks


# Add unique id to chunks
def calculate_chunk_ids(chunks):
  last_page_id = None
  current_chunk_index = 0

  for chunk in chunks:
    source = chunk.metadata.get("source")
    page = chunk.metadata.get("page")
    current_page_id = f"{source}:{page}"

    if current_page_id == last_page_id:
      current_chunk_index += 1
    else:
      current_chunk_index = 0

    chunk_id = f"{current_page_id}:{current_chunk_index}"
    last_page_id = current_page_id
    chunk.metadata["id"] = chunk_id

  print(f"Calculated chunk IDs for {len(chunks)} chunks.")
  return chunks
