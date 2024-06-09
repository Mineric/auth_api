from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from app.dependicies import Base
import re

class UserModel(Base):
    __tablename__ = "users"
    
    user_id = Column(String(20), primary_key=True, index=True)
    password = Column(String(20), nullable=False)
    nickname = Column(String(50), nullable=True)
    comment = Column(String(255), nullable=True)
    
    __table_args__ = (
        CheckConstraint("LENGTH(user_id) BETWEEN 6 AND 20", name="user_id_length"),
        CheckConstraint("LENGTH(password) BETWEEN 8 AND 20", name="password_length"),
    )
    
    def __init__(self, user_id, password, nickname=None, comment=None):
        self.validate_user_id(user_id)
        self.validate_password(password)
        self.user_id = user_id
        self.password = password
        self.nickname = nickname
        self.comment = comment

    @staticmethod
    def validate_user_id(user_id):
        if not re.match(r'^[a-zA-Z0-9]{6,20}$', user_id):
            raise ValueError("user_id must be 6-20 halfwidth alphanumeric characters.")

    @staticmethod
    def validate_password(password):
        if not re.match(r'^[\x21-\x7E]{8,20}$', password):  # \x21 to \x7E are printable ASCII characters excluding space
            raise ValueError("password must be 8-20 ASCII characters without spaces or control characters.")
