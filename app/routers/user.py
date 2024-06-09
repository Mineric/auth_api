from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import base64
from typing import Optional
from app import crud, schemas, dependicies

router = APIRouter()

@router.post("/signup", response_model=schemas.UserResponse, responses={400: {"model": schemas.ErrorResponse}})
def signup(user: schemas.User, db: Session = Depends(dependicies.get_db)):
    if not user.user_id or not user.password:
        raise HTTPException(status_code=400, detail={
            "message": "Account creation failed",
            "cause": "required user_id and password"
        })
    
    db_user = crud.get_user(db, user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail={
            "message": "Account creation failed",
            "cause": "already same user_id is used"
        })

    new_user = crud.create_user(db, user)
    return {
        "message": "Account successfully created",
        "user": {
            "user_id": new_user.user_id,
            "nickname": new_user.nickname
        }
    }

@router.get("/users/{user_id}", response_model=schemas.UserResponse, responses={404: {"model": schemas.ErrorResponse}})
def get_user(user_id: str, db: Session = Depends(dependicies.get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail={
            "message": "User not found",
            "cause": "Invalid user_id"
        })

    return {
        "message": "User found",
        "user": {
            "user_id": db_user.user_id,
            "nickname": db_user.nickname
        }
    }

@router.patch("/users/{user_id}", response_model=schemas.UserResponse, responses={404: {"model": schemas.ErrorResponse}})
def update_user(user_id: str, update: schemas.UpdateUser, db: Session = Depends(dependicies.get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail={
            "message": "User not found",
            "cause": "Invalid user_id"
        })

    updated_user = crud.update_user(db, user_id, update.nickname)
    return {
        "message": "User information updated",
        "user": {
            "user_id": updated_user.user_id,
            "nickname": updated_user.nickname
        }
    }

@router.post("/close", response_model=schemas.DeleteUserResponse, responses={401: {"model": schemas.AuthErrorResponse}})
def delete_user(request: Request, db: Session = Depends(dependicies.get_db)):
    auth_header: Optional[str] = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail={"message": "Missing or invalid Authorization header"})

    auth_header = auth_header[len("Basic "):]
    try:
        decoded_bytes = base64.b64decode(auth_header)
        decoded_str = decoded_bytes.decode("utf-8")
        user_id, password = decoded_str.split(":", 1)
    except Exception as e:
        raise HTTPException(status_code=401, detail={"message": "Invalid Authorization header format"})

    db_user = crud.get_user(db, user_id)
    if not db_user or db_user.password != password:
        raise HTTPException(status_code=401, detail={"message": "Invalid user_id or password"})

    crud.delete_user(db, user_id)
    return {"message": "Account and user successfully removed"}
