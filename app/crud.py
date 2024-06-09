from sqlalchemy.orm import Session
from app.models import UserModel
from app.schemas import User

def create_user(db: Session, user: User):
    db_user = UserModel(user_id=user.user_id, password=user.password, nickname=user.user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.user_id == user_id).first()

def update_user(db: Session, user_id: str, nickname: str):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if db_user:
        db_user.nickname = nickname
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
