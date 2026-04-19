from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from core.enhanced_retriever import retrieve_context
from core.generator import generate_answer, is_advisory_query, REFUSAL_PROMPT
from routers.metrics import router as metrics_router

app = FastAPI(title="Mutual Fund FAQ API", description="Facts-only RAG backend")

# Allow Next.js frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    thread_id: str
    query: str
    scheme_name: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    citation: Optional[str]
    last_updated: Optional[str]
    is_advisory: bool

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include metrics router
app.include_router(metrics_router)

@app.post("/api/chat/query", response_model=QueryResponse)
async def chat_query(req: QueryRequest):
    # 1. Refusal Engine (Guardrail Check)
    if is_advisory_query(req.query):
        return QueryResponse(
            answer=REFUSAL_PROMPT.strip(),
            citation=None,
            last_updated=None,
            is_advisory=True
        )

    # 2. Retriever Engine (Querying ChromaDB)
    context, citation, updated_date = retrieve_context(req.query, req.scheme_name, top_k=3)

    # 3. Generator Engine (OpenAI synthesized factual answer)
    answer = generate_answer(req.query, context)

    return QueryResponse(
        answer=answer,
        citation=citation if citation else None,
        last_updated=updated_date if updated_date else None,
        is_advisory=False
    )

# Run instructions:
# cd "apps/api"
# uvicorn main:app --reload
