from fastapi import APIRouter, HTTPException, Body
from app.services.rag_services import rag_pipeline

router = APIRouter()

@router.post("/query")
async def query(payload: dict = Body(...)):
    query_text = payload.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text is required")

    try:
        # Currently the pipeline is synchronous, so we call it directly.
        # If it becomes async in the future, we would await it.
        answer = rag_pipeline(query_text)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))