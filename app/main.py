from fastapi import FastAPI
from app.routes import query, ingest, health

app = FastAPI()

app.include_router(query.router)
app.include_router(ingest.router)
app.include_router(health.router)