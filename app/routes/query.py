from fastapi import APIRouter
from app.services.rag_service import get_answer

router = APIRouter()

@router.post("/query")
async def query(payload: dict):

    query = payload["query"]
    shard = "hr_general"

    answer = await get_answer(query, shard)

    return {"answer": answer}