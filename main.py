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
    text: str
    is_correct: bool

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
db_dependency = Annotated[Session, Depends(get_db)]

# create question along with choices
@app.post("/questions")
async def createQuestions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(text = question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(text = choice.text, is_correct = choice.is_correct, question_id = db_question.id)
        db.add(db_choice)
    db.commit()

# get a question based on id
@app.get("/questions/{question_id}")
async def readQuestion(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Question not found with given question id')
    return result

# get choices based on question id
@app.get("/choices/{question_id}")
async def readChoices(question_id, db:db_dependency):
    result = db.query(models.Choices).filter(question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='No choices found with given question Id')
    return result