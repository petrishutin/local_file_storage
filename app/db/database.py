import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

from app.settings import config

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "files",
    metadata,
    sqlalchemy.Column("hash_name", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("extension", sqlalchemy.String),
    sqlalchemy.Column("bucket", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
