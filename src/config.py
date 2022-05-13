import os


class Config:
    SECRET_KEY = os.urandom(32)


class DevelopmentConfig(Config):
    DEBUG = True
    DEFAULT_ITEM_PER_PAGE = 5
    MONGODB_SETTINGS = {
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": 27017,
        "db": "HIS",
    }


config = {
    "development": DevelopmentConfig,
    "testing": None,
    "production": None,
    "default": DevelopmentConfig,
}
