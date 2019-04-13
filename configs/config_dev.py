class Config(object):
    DEBUG = False
    TESTING = False
    # TODO: use in memory database for loopback test
    # DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://kyzysdphaqlzbb@ec2-54-221-201-212.compute-1.amazonaws.com/dfuqci9rqsdtb9'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'postgres://postgres@localhost:5432/helios'


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = ''
