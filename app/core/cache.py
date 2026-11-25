import json
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cache(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

def set_cache(key: str, value, ttl: int = 60):
    redis_client.setex(key, ttl, json.dumps(value, default=str))

def invalidate_cache_pattern(pattern: str):
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)