# Papermind — Evaluation-Driven RAG for Research Papers

A production-grade Retrieval-Augmented Generation (RAG) system built for researchers and students who need to query collections of academic papers. Upload your reading list, ask questions, and get answers with inline citations pointing to exact pages and source documents.

Built by Ahmad Hassan — Master's student in AI & NLP at Harbin Institute of Technology, Shenzhen. Developed as a real tool for my own thesis research on Urdu reasoning benchmarks (URBench).

---

## Problem Statement

Researchers working with large collections of papers face a real problem: finding specific information across dozens of PDFs is slow, keyword search misses context, and generic RAG systems hallucinate or return irrelevant chunks. Most portfolio RAG projects are tutorial-level — they work on one PDF with basic semantic search and no way to verify quality.

Papermind solves this with a multi-stage retrieval pipeline that combines keyword and semantic search, reranks results using a cross-encoder, and returns answers with page-level citations you can verify.

---

## Features

- Upload PDF, DOCX, MD, or TXT documents
- Hybrid retrieval — BM25 keyword search + dense vector similarity, fused via Reciprocal Rank Fusion
- Cross-encoder reranking — retrieves 20 candidates, reranks to top 5 before LLM call
- Inline citations — every answer references exact source document and page number
- Multi-document support — query across an entire corpus, not just one file
- Fast LLM answers via Groq (LLaMA 3.3 70B)
- Fully Dockerized — single command deployment
- Interactive API docs via FastAPI Swagger UI

---

## Architecture
User Query

│

▼

Hybrid Retrieval

├── BM25 (keyword)      ─┐

└── Dense (semantic)    ─┴─► Reciprocal Rank Fusion → 20 candidates

│

▼

Cross-Encoder Reranker (ms-marco-MiniLM-L-12-v2)

│ top 5 chunks

▼

Groq LLM (LLaMA 3.3 70B)

│

▼

Answer + Inline Citations [1] [2] [3]
---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Vector Store | ChromaDB |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Keyword Search | BM25 (rank-bm25) |
| Reranker | cross-encoder/ms-marco-MiniLM-L-12-v2 |
| LLM | Groq — LLaMA 3.3 70B |
| PDF Parsing | PyPDF + LangChain |
| Containerization | Docker + docker-compose |

---

## Project Structure
papermind/

├── app/

│   ├── core/           # Configuration and environment variables

│   ├── models/         # Pydantic request/response schemas

│   ├── routes/         # API endpoints (health, upload, query)

│   ├── services/

│   │   ├── ingest_service.py          # Document loading, chunking, embedding

│   │   ├── hybrid_retrieval_service.py # BM25 + dense + RRF fusion

│   │   ├── rerank_service.py          # Cross-encoder reranking

│   │   └── rag_service.py             # LLM answer generation

│   └── utils/          # File handling helpers

├── data/

│   ├── uploads/        # Uploaded documents

│   └── chroma_db/      # Persisted vector store

├── frontend/           # Streamlit UI

├── screenshots/        # Demo screenshots

├── Dockerfile

├── docker-compose.yml

└── requirements.txt

---

## Quick Start

### With Docker (recommended)

```bash
git clone https://github.com/ahmadhassan22/papermind.git
cd papermind
cp .env.example .env
# Add your GROQ_API_KEY to .env
docker compose up --build
```

API available at `http://localhost:8000`
Swagger UI at `http://localhost:8000/docs`

### Without Docker

```bash
git clone https://github.com/ahmadhassan22/papermind.git
cd papermind
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
python run.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root health check |
| GET | `/health` | Service status |
| POST | `/upload` | Upload and index a document |
| POST | `/query` | Query indexed documents |

### Example Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What evaluation benchmarks are used for multilingual NLP?"}'
```

Response includes answer with inline citations and source metadata (filename + page number).

---

## Engineering Decisions

**Why hybrid retrieval instead of pure semantic search?**
Research papers contain technical terms, model names, and acronyms (e.g., "BLEU", "MaLA500", "SIB200") that semantic search can miss. BM25 catches exact keyword matches while dense vectors handle meaning. Reciprocal Rank Fusion combines both ranked lists without requiring score normalization.

**Why a cross-encoder reranker?**
Bi-encoders (used for initial retrieval) encode query and document independently — fast but less accurate. A cross-encoder reads both together and scores relevance more precisely. We retrieve 20 candidates cheaply, then rerank to top 5 accurately. This improves answer quality and reduces LLM context size, cutting latency.

**Why Groq instead of local Ollama?**
Ollama requires a 4GB+ local model download and CPU inference is too slow for a responsive API. Groq's free tier provides 30 req/min at ~500 tokens/sec — fast enough for real use, zero infrastructure cost, and trivially swappable via an environment variable.

**Why chunk_size=1000 with overlap=200?**
Research paper paragraphs average 600–900 characters. The original 500-character chunks were splitting sentences mid-way, breaking context. 1000 characters preserves paragraph integrity; 200-character overlap ensures context isn't lost at chunk boundaries.

**Why persist ChromaDB to a Docker volume?**
Without a volume mount, every container restart wipes the indexed documents. Mounting `./data` means uploads and embeddings survive restarts — essential for any real deployment.

---

## Screenshots

![Swagger UI](screenshots/swagger_ui.png)
![Upload Success](screenshots/upload_success.png)
![Query with Citations](screenshots/query_with_citations.png)

---

## Author

**Ahmad Hassan**
Master's Student — AI & NLP, Harbin Institute of Technology Shenzhen
[GitHub](https://github.com/ahmadhassan22) | [LinkedIn](https://linkedin.com/in/ahmadhassan22)