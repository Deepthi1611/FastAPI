from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'postgresql://postgres:Deepthi%40134@localhost:5432/Blog'
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()