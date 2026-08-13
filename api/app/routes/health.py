from flask import Blueprint, jsonify

from app import extensions

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@health_bp.get("/ready")
def ready():
    checks: dict[str, str] = {}

    try:
        if extensions.mongo_client is None:
            raise RuntimeError("MongoDB client is not initialized")
        extensions.mongo_client.admin.command("ping")
        checks["mongodb"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["mongodb"] = str(exc)

    try:
        if extensions.redis_client is None:
            raise RuntimeError("Redis client is not initialized")
        if not extensions.redis_client.ping():
            raise RuntimeError("Redis ping failed")
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = str(exc)

    is_ready = all(value == "ok" for value in checks.values())
    status_code = 200 if is_ready else 503

    return jsonify({"status": "ready" if is_ready else "not_ready", **checks}), status_code
