from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_chroma import Chroma

from app.config import LLM_MODEL

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str, database_path: str, embeddings):
  db = Chroma(persist_directory=database_path, embedding_function=embeddings)

  results = db.similarity_search_with_score(query_text, k=5)
  context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

  prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
  prompt = prompt_template.format(context=context_text, question=query_text)

  model = Ollama(model=LLM_MODEL)
  response_text = model.invoke(prompt)

  sources = [doc.metadata.get("id", None) for doc, _score in results]
  formatted_response = f"Response: {response_text}\nSources: {sources}"
  print(formatted_response)
  return response_text
