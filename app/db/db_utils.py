from sqlalchemy.orm import Session

from app.db.models import FileMetaData


def select_file_data(db: Session, hash_name: str):
    return db.query(FileMetaData).filter(FileMetaData.hash_name == hash_name).first()


def insert_file_data(db: Session, hash_name: str, extension: str, bucket: str):
    new_file = FileMetaData(hash_name=hash_name, extension=extension, bucket=bucket)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def update_file_extension(db: Session, hash_name: str, extension: str):
    file: FileMetaData = db.query(FileMetaData).filter(FileMetaData.hash_name == hash_name).first()
    file.extension = extension
    db.commit()
    db.refresh(file)
    return file
