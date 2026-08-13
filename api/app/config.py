import os
from pathlib import Path


def read_secret(name: str, default: str = "") -> str:
    file_path = os.getenv(f"{name}_FILE")
    if file_path:
        path = Path(file_path)
        if path.is_file():
            return path.read_text(encoding="utf-8").strip()

    return os.getenv(name, default)


class Config:
    SECRET_KEY = read_secret("SECRET_KEY")

    MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "app")
    MONGODB_USER = os.getenv("MONGODB_USER", "appuser")
    MONGODB_PASSWORD = read_secret("MONGODB_PASSWORD")
    MONGODB_AUTH_SOURCE = os.getenv("MONGODB_AUTH_SOURCE", "admin")

    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))

    ITEMS_CACHE_KEY = "items:all"
