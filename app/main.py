from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, upload, query

app = FastAPI(
    title="Papermind API",
    version="1.0.0",
    description="Evaluation-driven RAG system for research paper Q&A"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Papermind backend is running"}

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(query.router)