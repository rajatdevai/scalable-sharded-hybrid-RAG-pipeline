from fastapi import APIRouter, HTTPException, Body
from workers.queue import push_to_queue

router = APIRouter()

@router.post("/ingest")
async def ingest(payload: dict = Body(...)):
    docs = payload.get("documents")
    if not docs or not isinstance(docs, list):
        raise HTTPException(status_code=400, detail="A list of documents is required")

    try:
        push_to_queue(docs)
        return {
            "status": "queued", 
            "message": f"Successfully queued {len(docs)} documents for background processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
