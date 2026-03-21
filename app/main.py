from fastapi import FastAPI
from app.routes import health, upload, query

app = FastAPI(
    title = "RAG API Project",
    version = "1.0.0"
)

@app.get("/")
def root():
    return {"message": "RAG backend is running"}

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(query.router)
