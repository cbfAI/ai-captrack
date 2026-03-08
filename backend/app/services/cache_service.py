import redis
import json
from typing import Optional, Any
from app.core.config import settings


class CacheService:
    def __init__(self):
        if settings.REDIS_URL.startswith("memory://"):
            self._cache = {}
        else:
            self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.ttl_capabilities = settings.CACHE_TTL_CAPABILITIES
        self.ttl_llm_parse = settings.CACHE_TTL_LLM_PARSE

    def get(self, key: str) -> Optional[Any]:
        if hasattr(self, '_cache'):
            return self._cache.get(key)
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if hasattr(self, '_cache'):
            self._cache[key] = value
        else:
            self.redis_client.set(key, json.dumps(value), ex=ttl)

    def delete(self, key: str):
        if hasattr(self, '_cache'):
            self._cache.pop(key, None)
        else:
            self.redis_client.delete(key)

    def get_capabilities_cache(self, page: int, page_size: int, filters_hash: str) -> Optional[Any]:
        key = f"capabilities:list:{page}:{page_size}:{filters_hash}"
        return self.get(key)

    def set_capabilities_cache(self, page: int, page_size: int, filters_hash: str, data: Any):
        key = f"capabilities:list:{page}:{page_size}:{filters_hash}"
        self.set(key, data, self.ttl_capabilities)

    def get_llm_parse_cache(self, content_hash: str) -> Optional[Any]:
        key = f"llm:parse:{content_hash}"
        return self.get(key)

    def set_llm_parse_cache(self, content_hash: str, data: Any):
        key = f"llm:parse:{content_hash}"
        self.set(key, data, self.ttl_llm_parse)

    def invalidate_capabilities_cache(self):
        if hasattr(self, '_cache'):
            keys_to_delete = [k for k in self._cache if k.startswith("capabilities:list:")]
            for key in keys_to_delete:
                del self._cache[key]
        else:
            keys = self.redis_client.keys("capabilities:list:*")
            if keys:
                self.redis_client.delete(*keys)


cache_service = CacheService()
