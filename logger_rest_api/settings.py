# Flask settings
FLASK_SERVER_NAME = '192.168.1.180:80'
FLASK_DEBUG = True  # Do not use debug mode in production
FLASK_ENV = 'development'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///records.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
