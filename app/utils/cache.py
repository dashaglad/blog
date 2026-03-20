import json
from typing import Any

from app.core.config import settings
from app.core.redis import redis_client


class Cache:
    @staticmethod
    def get(key: str) -> Any | None:
        cached = redis_client.get(key)
        if cached is None or cached == "":
            return None
        return json.loads(cached)

    @staticmethod
    def set(key: str, value: Any, ttl: int | None = None) -> None:
        redis_client.set(
            key,
            json.dumps(value),
            ex=ttl if ttl is not None else settings.CACHE_TTL,
        )

    @staticmethod
    def delete(key: str) -> None:
        redis_client.delete(key)

