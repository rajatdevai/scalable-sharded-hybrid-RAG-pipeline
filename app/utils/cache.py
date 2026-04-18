import redis 
import json
from app.config.settings import REDIS_URL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception:
        return None

def set_cache(key, value):
    try:
        redis_client.set(key, json.dumps(value), ex=3600)
    except Exception:
        pass