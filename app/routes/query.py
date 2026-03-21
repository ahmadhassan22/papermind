from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import answer_question

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_docs(request: QueryRequest):
    answer, sources = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }  