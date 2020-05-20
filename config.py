class Config(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "My Super Secret Key"
    SERVER_NAME = "127.0.0.1:5000"
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    
class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
    
    
