import json
from typing import Any

from app import extensions


def get_cached_json(key: str) -> Any | None:
    if extensions.redis_client is None:
        return None

    cached = extensions.redis_client.get(key)
    if cached is None:
        return None

    return json.loads(cached)


def set_cached_json(key: str, value: Any, ttl_seconds: int) -> None:
    if extensions.redis_client is None:
        return

    extensions.redis_client.setex(key, ttl_seconds, json.dumps(value))


def delete_cached(key: str) -> None:
    if extensions.redis_client is None:
        return

    extensions.redis_client.delete(key)
