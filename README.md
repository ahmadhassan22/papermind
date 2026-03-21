# RAG Document Retrieval API

A modular FastAPI backend for document ingestion, semantic retrieval, and retrieval-augmented question answering over uploaded PDF files.

## Features
- Upload PDF documents via API
- Parse and chunk PDF text
- Generate embeddings using Sentence Transformers
- Store vectors in ChromaDB
- Retrieve relevant chunks for user queries
- Generate context-aware answers using a local LLM with Ollama
- Interactive API testing with FastAPI Swagger UI

## Tech Stack
- Python
- FastAPI
- LangChain
- ChromaDB
- Sentence Transformers
- Ollama
- Pydantic

## Project Structure
app/
  routes/      # API endpoints
  services/    # ingestion, retrieval, and RAG logic
  models/      # request/response schemas
  core/        # config
  utils/       # helper functions

## API Endpoints
	•	GET / - root endpoint
	•	GET /health - health check
	•	POST /upload - upload and index a PDF
	•	POST /query - retrieve relevant context and generate answer  

## Example Workflow
	1.	Upload a PDF document
	2.	Backend parses and chunks the document
	3.	Chunks are embedded and stored in ChromaDB
	4.	User submits a question
	5.	System retrieves top relevant chunks
	6.	Local LLM generates an answer using retrieved context    

## Run Locally

1. Install dependencies   
pip install -r requirements.txt

2. Start the FastAPI server
python run.py

3. Open Swagger UI
http://127.0.0.1:8000/docs

## Screenshots

Add Swagger UI and successful query screenshots in the screenshots/ folder.

## Future Improvements
	•	Dockerize the application
	•	Add authentication
	•	Add support for more document types
	•	Add cloud deployment
	•	Improve answer quality with reranking or hybrid retrieval

## Author

Ahmad Hassan
Master’s Student (AI & NLP)
Harbin Institute of Technology, Shenzhen  