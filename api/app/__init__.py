from flask import Flask

from app.config import Config
from app.extensions import init_extensions
from app.routes import register_routes


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_extensions(app)
    register_routes(app)
    return app
