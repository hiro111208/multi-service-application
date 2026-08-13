from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from flask import current_app
from pymongo.collection import Collection

from app import extensions
from app.services.cache import delete_cached, get_cached_json, set_cached_json


def _items_collection() -> Collection:
    if extensions.mongo_db is None:
        raise RuntimeError("MongoDB is not initialized")

    return extensions.mongo_db["items"]


def serialize_item(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(document["_id"]),
        "name": document["name"],
        "created_at": document["created_at"],
    }


def list_items() -> list[dict[str, Any]]:
    cache_key = current_app.config["ITEMS_CACHE_KEY"]
    cached = get_cached_json(cache_key)
    if cached is not None:
        return cached

    documents = _items_collection().find().sort("created_at", -1)
    items = [serialize_item(document) for document in documents]
    set_cached_json(cache_key, items, current_app.config["CACHE_TTL_SECONDS"])
    return items


def create_item(name: str) -> dict[str, Any]:
    document = {
        "name": name.strip(),
        "created_at": datetime.now(UTC).isoformat(),
    }
    result = _items_collection().insert_one(document)
    document["_id"] = result.inserted_id

    delete_cached(current_app.config["ITEMS_CACHE_KEY"])
    return serialize_item(document)


def get_item(item_id: str) -> dict[str, Any] | None:
    if not ObjectId.is_valid(item_id):
        return None

    document = _items_collection().find_one({"_id": ObjectId(item_id)})
    if document is None:
        return None

    return serialize_item(document)
