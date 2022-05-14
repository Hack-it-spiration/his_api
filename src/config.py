import os


class Config:
    SECRET_KEY = os.urandom(32)
    DEFAULT_ITEM_PER_PAGE = 5
    DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": 27017,
        "db": "HIS",
    }


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        "host": os.getenv("MONGODB_SETTINGS"),
    }
    WEATHERKEY = "ca5bb720e4bc43c5d80d9aab5b963c7d"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": None,
    "default": TestingConfig,
}
