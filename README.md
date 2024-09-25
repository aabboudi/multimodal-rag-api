# Multimodal RAG System for LLMs

This project implements a multimodal RAG (Retrieval-Augmented Generation) system for large language models, enabling you to query files through API endpoints. Visit [rag.ipynb](notebook/rag.ipynb) for a step-by-step guide on how RAG operates, including examples and expected outcomes. Feel free to start there.

### Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/): to build the API
- [LangChain](https://www.langchain.com/): to manage language model interactions
- [Chroma](https://www.trychroma.com/): to store and handle multimodal data

### Installation

Clone the repo
```bash
git clone https://github.com/aabboudi/multimodal-rag-api.git
cd multimodal-rag-api
```

Create and activate a virtual environment
```bash
python -m venv venv
\venv\Scripts\activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run the server
```bash
fastapi dev app/main.py
```

### Usage

After running the server, you can send queries to the API endpoints to interact with the multimodal RAG system. Queries can be sent through the docs, Postman, or the command line.
