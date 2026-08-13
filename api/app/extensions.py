from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database
from redis import Redis

mongo_client: MongoClient | None = None
mongo_db: Database | None = None
redis_client: Redis | None = None


def init_extensions(app: Flask) -> None:
    global mongo_client, mongo_db, redis_client

    mongo_kwargs: dict = {
        "host": app.config["MONGODB_HOST"],
        "port": app.config["MONGODB_PORT"],
        "serverSelectionTimeoutMS": 3000,
    }

    username = app.config["MONGODB_USER"]
    password = app.config["MONGODB_PASSWORD"]
    if username and password:
        mongo_kwargs["username"] = username
        mongo_kwargs["password"] = password
        mongo_kwargs["authSource"] = app.config["MONGODB_AUTH_SOURCE"]

    mongo_client = MongoClient(**mongo_kwargs)
    mongo_db = mongo_client[app.config["MONGODB_DATABASE"]]

    redis_client = Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=app.config["REDIS_DB"],
        decode_responses=True,
        socket_connect_timeout=3,
    )
