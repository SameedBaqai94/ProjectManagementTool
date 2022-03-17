from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='postgresql://postgres:Shadow_12@127.0.0.1/fastapi'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

Session_local=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

# Dependency
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()