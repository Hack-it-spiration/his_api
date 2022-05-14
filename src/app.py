from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from src.config import config
from src.features.common.response_handlers import error_handlers
from src.features.ml_model.blueprint import model as model_blueprint
from src.features.toll_roads.checkpoint.blueprint import (
    checkpoints as checkpoints_blueprint,
)
from src.features.toll_roads.segment.blueprint import segments as segments_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, ressources={r"*": {"origins": "*"}})
    db = MongoEngine()
    db.init_app(app)
    app.register_blueprint(checkpoints_blueprint)
    app.register_blueprint(segments_blueprint)
    app.register_blueprint(model_blueprint)
    for error, handler in error_handlers.items():
        app.register_error_handler(error, handler)
    return app
