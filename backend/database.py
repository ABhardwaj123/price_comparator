from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("database_url")

#this creates actual connection with database
engine = create_engine(database_url)

#bind=engine tells which database it is using
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)


Base = declarative_base()

#this function is called whenever a route needs access to db
def get_db():

    #creating a fresh session for each request
    db = SessionLocal()

    try:
        #gives control to that particular route that needs access
        yield db
    finally:
        db.close()




#sessionmaker is the factory/parent that creates database sessions
#declarative_base gives you a base class 