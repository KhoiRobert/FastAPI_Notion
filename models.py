from sqlalchemy import Boolean, String ,Column, Integer, DateTime
from sqlalchemy.sql import func
from uuid import uuid4
from database import Base


class Todo(Base):
    __tablename__ = "todos"#11

    id = Column(Integer, primary_key=True, index=True )#12
    title =Column(String)
    complete = Column(Boolean, default=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())#13

