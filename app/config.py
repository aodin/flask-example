class Default:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''
    # Connection format: dialect+driver://username:password@host:port/database
    # e.g. for PostGres postgresql://user:password@host/database
    # e.g. for local SQLite 'sqlite:////tmp/test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class Development(Default):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
