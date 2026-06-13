from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import health, upload, query
import os

app = FastAPI(
    title="Papermind API",
    version="1.0.0",
    description="Evaluation-driven RAG system for research paper Q&A"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(query.router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend-react", "dist")

if os.path.exists(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/")
    @app.head("/")
    def serve_frontend():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
else:
    @app.get("/")
    @app.head("/")
    def root():
        return {"message": "Papermind backend is running"}