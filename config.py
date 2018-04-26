# This file contains the application's configurations


class Config(object):
    """
    Common configurations
    """


class DevelopmentConfig(Config):
    """
    Development Configurations
    """
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'mysql://mucs:mucs@localhost/test'
    SQLALCHEMY_ECHO = True
    PORT = "8085"


class ProductionConfig(Config):
    """
    Production Configurations
    """
    Debug = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}