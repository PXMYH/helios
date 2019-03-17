class Config(object):
    DEBUG = False
    TESTING = False
    # TODO: use in memory database for loopback test
    # DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'postgres://postgres@localhost:5432/helios'


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = ''
