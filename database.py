from sqlalchemy import create_engine #create engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Khoi2921432@localhost/firstDataProject"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit =False,bind=engine)
Base = declarative_base()