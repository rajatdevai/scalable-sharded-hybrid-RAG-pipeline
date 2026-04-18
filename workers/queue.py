import json
import redis
from app.config.settings import REDIS_URL
from app.config.constants import INGEST_QUEUE

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def push_to_queue(docs):
    """
    Pushes a list of documents to the ingestion queue.
    """
    if not isinstance(docs, list):
        docs = [docs]
        
    for doc in docs:
        redis_client.rpush(INGEST_QUEUE, json.dumps({"text": doc}))

def pop_from_queue():
    """
    Pops a document from the ingestion queue.
    Returns None if queue is empty.
    """
    data = redis_client.lpop(INGEST_QUEUE)
    return json.loads(data) if data else None

def get_queue_size():
    """
    Returns the current size of the ingestion queue.
    """
    return redis_client.llen(INGEST_QUEUE)
