from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# url of the database created
# postgresql://<username>:<password>@<host>:<port>/<database_name>
URL_DATABASE = 'postgresql://postgres:Deepthi%40134@localhost:5432/QuizApplication'

# The engine is the starting point for any SQLAlchemy application. It is responsible for:

# Managing the connection to the database.
# Translating Python code to SQL queries.
# Executing the queries against the PostgreSQL database

# create engine
engine = create_engine(URL_DATABASE)

# sessionmaker is a factory for creating sessions. A session is used to interact with the database and perform operations like querying, inserting, and updating records.
# autocommit=False: This disables automatic committing of transactions. You will need to manually commit any changes to the database.
# autoflush=False: This prevents automatic flushing of the session, meaning changes won’t be written to the database unless explicitly told to.
# bind=engine: This binds the session to the engine so it knows which database connection to use.

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# declarative_base() is a factory function that returns a base class.
# You will use this Base class as the parent class for all your ORM models. These ORM models will represent your database tables in Python.
# Any class that inherits from Base will automatically be linked to the PostgreSQL database, and SQLAlchemy will map it to the corresponding table.

Base = declarative_base()