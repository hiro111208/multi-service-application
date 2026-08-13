import mongomock
import pytest
from fakeredis import FakeRedis
from flask import Flask

from app import create_app
from app import extensions


def _init_test_extensions(app: Flask) -> None:
    extensions.mongo_client = mongomock.MongoClient()
    extensions.mongo_db = extensions.mongo_client[app.config["MONGODB_DATABASE"]]
    extensions.redis_client = FakeRedis(decode_responses=True)


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr("app.init_extensions", _init_test_extensions)
    application = create_app()
    application.config.update(
        {
            "TESTING": True,
            "MONGODB_DATABASE": "test",
            "CACHE_TTL_SECONDS": 60,
        }
    )

    with application.app_context():
        yield application


@pytest.fixture
def client(app):
    return app.test_client()
