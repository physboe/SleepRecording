from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from recording_rest_api.database.recording import DaoRecordSession  # noqa
    db.drop_all()
    db.create_all()
