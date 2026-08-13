from flask import Blueprint, jsonify, request

from app.services.items import create_item, get_item, list_items

items_bp = Blueprint("items", __name__)


@items_bp.get("/items")
def get_items():
    return jsonify({"items": list_items()}), 200


@items_bp.get("/items/<item_id>")
def get_item_by_id(item_id: str):
    item = get_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@items_bp.post("/items")
def post_item():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Field 'name' is required"}), 400

    item = create_item(name)
    return jsonify(item), 201
