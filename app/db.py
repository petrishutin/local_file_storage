import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.settings import config

metadata = sqlalchemy.MetaData()

Base = declarative_base()


class FileMetaData(Base):
    __tablename__ = 'file_meta'
    hash_name = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True)
    extension = sqlalchemy.Column(sqlalchemy.String)
    bucket = sqlalchemy.Column(sqlalchemy.String)


engine = sqlalchemy.create_engine(
    config.DB_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Init DB at startup"""
    Base.metadata.create_all(bind=engine)


# DB utils ==================================

def select_file_data(db: Session, file_hash: str):
    return db.query(FileMetaData).filter(FileMetaData.hash_name == file_hash).first()


def insert_file_meta(db: Session, file_hash: str, extension: str, bucket: str):
    new_file = FileMetaData(hash_name=file_hash, extension=extension, bucket=bucket)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def update_file_extension(db: Session, file_hash: str, extension: str):
    file: FileMetaData = db.query(FileMetaData).filter(FileMetaData.hash_name == file_hash).first()
    file.extension = extension
    db.commit()
    db.refresh(file)
    return file


def delete_file_record(db: Session, file_hash: str):
    db.query(FileMetaData).filter(FileMetaData.hash_name == file_hash).delete()
    db.commit()
    return file_hash
