from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from app.dependicies import Base

# Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    password = Column(String)
    nickname = Column(String)
