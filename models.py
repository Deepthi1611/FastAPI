from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

# defining Questions model
class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)

# defining Choices model
class Choices(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey(Questions.id))