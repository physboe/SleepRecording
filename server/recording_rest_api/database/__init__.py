from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()
log = logging.getLogger(__name__)


def reset_database():
    log.info("Setting up database")
    from recording_rest_api.database.recording import DaoRecordSession, DaoHrmRecord  # noqa
    db.drop_all()
    db.create_all()
