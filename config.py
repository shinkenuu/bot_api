class Config(object):
    DB_HOST = 'localhost'
    DB_PORT = 27017


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_NAME = 'test_bot_api'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    CSRF_ENABLED = False
    DB_NAME = 'test_bot_api'


class ProductionConfig(Config):
    DEBUG = False
    DB_NAME = 'bot_api'


app_config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
}
