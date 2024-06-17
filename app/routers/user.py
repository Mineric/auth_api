# import base64
# from fastapi import APIRouter, Depends, HTTPException, Header
# from sqlalchemy.orm import Session
# from app import crud, schemas
# from app.dependicies import get_db

# router = APIRouter()

# def authenticate_user(auth_header: str = Header(...)):
#     try:
#         auth_type, encoded_credentials = auth_header.split()
#         if auth_type.lower() != 'basic':
#             raise HTTPException(status_code=401, detail="Unsupported authentication type. Only Basic authentication is supported.")
#         decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
#         username, password = decoded_credentials.split(':')
#         return username, password
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Authentication Failed")

# def validate_user(user: schemas.CreateUser):
#     try:
#         user = schemas.CreateUser(**user.dict())
#         if not user:
#             raise HTTPException(status_code=400, detail={
#                 "message": "Account creation failed",
#                 "cause": "required user_id and password"
#             })
#         if not user.user_id or not user.password:
#             raise HTTPException(status_code=400, detail={
#                 "message": "Account creation failed",
#                 "cause": "required user_id and password"
#             })
#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail={"message": "Account creation failed", "cause": str(ve)})

# @router.post("/signup", response_model=schemas.UserResponse)
# def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
#     validate_user(user)
#     if not user.user_id or not user.password:
#         raise HTTPException(status_code=400, detail={
#             "message": "Account creation failed",
#             "cause": "required user_id and password"
#         })

#     db_user = crud.get_user(db, user.user_id)
#     if db_user:
#         raise HTTPException(status_code=400, detail="User already registered")
#     new_user = crud.create_user(db, user)
#     # return {"message": "User created successfully", "user": new_user.__dict__}
#     return {
#         "message": "Account successfully created",
#         "user": {
#             "user_id": new_user.user_id,
#             "nickname": new_user.nickname
#         }
#     }

# @router.get("/users/{user_id}", response_model=schemas.UserResponse)
# def read_user(user_id: str, auth: tuple = Depends(authenticate_user), db: Session = Depends(get_db)):
#     username, password = auth
#     db_user = crud.get_user(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     # Basic Authorization check
#     if db_user.user_id != username or db_user.password != password:
#         raise HTTPException(status_code=401, detail="Unauthorized access")
#     # return {"message": "User retrieved successfully", "user": db_user.__dict__}
#     return {
#         "message": "User details by user_id",
#         "user": {
#             "user_id": db_user.user_id,
#             "nickname": db_user.nickname,
#             "comment": db_user.comment
#         }
#     }

# @router.patch("/users/{user_id}", response_model=schemas.UpdateUserResponse)
# def update_user(user_id: str, user_update: schemas.UpdateUser, auth: tuple = Depends(authenticate_user), db: Session = Depends(get_db)):
#     username, password = auth
#     updated_user = crud.get_user(db, user_id)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail="No User found")
#     # Basic Authorization check
#     if updated_user.user_id != username or updated_user.password != password:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
#     # Update user
#     updated_user.nickname = user_update.nickname
#     updated_user.comment = user_update.comment
#     db.commit()
#     db.refresh(updated_user)
#     #return {"message": "User updated successfully", "user": updated_user.__dict__}
#     return {
#         "message": "User successfully updated",
#         "recipe": [
#             {
#                 "nickname": updated_user.nickname,
#                 "comment": updated_user.comment
#             }
#         ]
#     }

# @router.post("/users/{user_id}", response_model=schemas.DeleteUserResponse)
# def delete_user(user_id: str, auth: tuple = Depends(authenticate_user), db: Session = Depends(get_db)):
#     username, password = auth
#     deleted_user = crud.delete_user(db, user_id)
#     if deleted_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     # Basic Authorization check
#     if deleted_user.user_id != username or deleted_user.password != password:
#         raise HTTPException(status_code=403, detail="Unauthorized access")
#     return {"message": "User deleted successfully"}



import base64
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependicies import get_db

router = APIRouter()

def authenticate_user(auth_header: str = Header(...)):
    try:
        auth_type, encoded_credentials = auth_header.split()
        if auth_type.lower() != 'basic':
            raise HTTPException(status_code=401, detail="Unsupported authentication type. Only Basic authentication is supported.")
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')
        return username, password
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication Failed")

def validate_user(user: schemas.CreateUser):
    try:
        # Create a validated user object from input
        validated_user = schemas.CreateUser(**user.dict())

        # Check if user object is empty
        if not validated_user:
            raise HTTPException(status_code=400, detail={
                "message": "Account creation failed",
                "cause": "required user_id and password"
            })

        # Check if user_id or password is missing
        if not validated_user.user_id or not validated_user.password:
            raise HTTPException(status_code=400, detail={
                "message": "Account creation failed",
                "cause": "required user_id and password"
            })

    except ValidationError:
        raise HTTPException(status_code=400, detail={
            "message": "Account creation failed",
            "cause": "required user_id and password"
        })

@router.post("/signup", response_model=schemas.UserResponse, responses={
    200: {"description": "Successful response", "model": schemas.UserResponse},
    400: {"description": "Bad request", "model": schemas.ErrorResponse},
    401: {"description": "Unauthorized", "model": schemas.AuthErrorResponse}
})
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    validate_user(user)
    if not user.user_id or not user.password:
        raise HTTPException(status_code=400, detail={
            "message": "Account creation failed",
            "cause": "required user_id and password"
        })

    db_user = crud.get_user(db, user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    new_user = crud.create_user(db, user)
    return {
        "message": "Account successfully created",
        "user": {
            "user_id": new_user.user_id,
            "nickname": new_user.nickname
        }
    }

@router.get("/users/{user_id}", response_model=schemas.UserResponse, responses={
    200: {"description": "Successful response", "model": schemas.UserResponse},
    400: {"description": "Bad request", "model": schemas.ErrorResponse},
    401: {"description": "Unauthorized", "model": schemas.AuthErrorResponse}
})
def read_user(user_id: str, auth: tuple = Depends(authenticate_user), db: Session = Depends(get_db)):
    username, password = auth
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.user_id != username or db_user.password != password:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return {
        "message": "User details by user_id",
        "user": {
            "user_id": db_user.user_id,
            "nickname": db_user.nickname,
            "comment": db_user.comment
        }
    }

@router.patch("/users/{user_id}", response_model=schemas.UpdateUserResponse, responses={
    200: {"description": "Successful response", "model": schemas.UpdateUserResponse},
    400: {"description": "Bad request", "model": schemas.ErrorResponse},
    401: {"description": "Unauthorized", "model": schemas.AuthErrorResponse}
})
def update_user(user_id: str, user_update: schemas.UpdateUser, auth: tuple = Depends(authenticate_user), db: Session = Depends(get_db)):
    username, password = auth
    updated_user = crud.get_user(db, user_id)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="No User found")
    if updated_user.user_id != username or updated_user.password != password:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    updated_user.nickname = user_update.nickname
    updated_user.comment = user_update.comment
    db.commit()
    db.refresh(updated_user)
    return {
        "message": "User successfully updated",
        "recipe": [
            {
                "nickname": updated_user.nickname,
                "comment": updated_user.comment
            }
        ]
    }

@router.post("/users/{user_id}", response_model=schemas.DeleteUserResponse, responses={
    200: {"description": "Successful response", "model": schemas.DeleteUserResponse},
    400: {"description": "Bad request", "model": schemas.ErrorResponse},
    401: {"description": "Unauthorized", "model": schemas.AuthErrorResponse}
})
def delete_user(user_id: str, auth: tuple = Depends(authenticate_user), db: Session = Depends(get_db)):
    username, password = auth
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if deleted_user.user_id != username or deleted_user.password != password:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return {"message": "User deleted successfully"}
