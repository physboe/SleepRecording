# Flask settings
SERVER_NAME = 'localhost:8888'
DEBUG = False  # Do not use debug mode in production
ENV = 'development'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# Ble Hrm settings
DEVICE_MAC = "0C:8C:DC:09:FE:6E"
DEVICE_CONNECTION_TYPE = "public"
GATTTOOL_DEBUG = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../records.sqlite'
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
