from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ


if "sqlite" in environ.get("DATABASE_URL"):
    engine = create_engine(
        environ.get("DATABASE_URL"), connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(environ.get("DATABASE_URL"), pool_recycle=60)


Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


def create_all():
    global Base
    global engine
    Base.metadata.create_all(engine)
