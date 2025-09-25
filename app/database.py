from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import SQLALCHEMY_DB_URL


def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()


engine = create_engine(SQLALCHEMY_DB_URL)
metaData = MetaData()

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
