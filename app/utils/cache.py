import redis 
import json
from app.config.settings import REDIS_HOST,REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, db=0)

def get_cache(key):
    value = redis_client.get(key)
    return json.loads(value) if value else None

def set_cache(key, value):
    redis_client.set(key, json.dumps(value), ex=3600)