from sqlalchemy.orm import Session

from app.db.models import FileMetaData


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
