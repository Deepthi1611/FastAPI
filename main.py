from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
# the below line creates all of the tables along with columns in postgres 
models.Base.metadata.create_all(bind = engine)

class ChoiceBase(BaseModel):
    choice: str
    isCorrect: bool

class QuestionBase(BaseModel):
    text:str
    choices: List[ChoiceBase]

# This function creates a new database session using the SessionLocal class (which is typically a session factory bound to the SQLAlchemy engine).
# Yield: This function uses a generator to yield a session instance. This allows FastAPI to manage the database session lifecycle automatically.
# Finally Block: The session is closed after the request is complete, ensuring that resources are freed up and avoiding potential memory leaks.

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


# The line defines db_dependency as an alias for a type that expects a Session, along with a specific dependency (in this case, get_db) that FastAPI will use to resolve that type during request handling.
# When used in a FastAPI route, it informs FastAPI to use the get_db function to provide a database session automatically whenever a parameter of type db_dependency is required in a route function.
db_dependency = Annotated[Session, get_db]