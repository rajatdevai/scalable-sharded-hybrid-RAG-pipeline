from fastapi import APIRouter
from app.services.ingestion_service import ingest_documents

router = APIRouter()

@router.post("/ingest")
def ingest(payload: dict):

    docs = payload["documents"]

    ingest_documents(docs)

    return {"status": "ingested"}