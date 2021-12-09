import sqlalchemy

from app.db.database import Base


class FileMetaData(Base):
    __tablename__ = 'file_meta'
    hash_name = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True)
    extension = sqlalchemy.Column(sqlalchemy.String)
    bucket = sqlalchemy.Column(sqlalchemy.String)
