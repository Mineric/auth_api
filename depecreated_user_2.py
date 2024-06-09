from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from app.utils.exceptions import CustomHTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
import base64
from typing import Optional
from app import crud, schemas, dependicies

router = APIRouter()
security = HTTPBasic()

# @router.post("/signup", response_model=schemas.UserResponse, responses={400: {"model": schemas.ErrorResponse}})
# def signup(user: schemas.User, db: Session = Depends(dependicies.get_db)):
#     if not user.user_id or not user.password:
#         raise HTTPException(status_code=400, detail={
#             "message": "Account creation failed",
#             "cause": "required user_id and password"
#         })
    
#     db_user = crud.get_user(db, user.user_id)
#     if db_user:
#         raise HTTPException(status_code=400, detail={
#             "message": "Account creation failed",
#             "cause": "already same user_id is used"
#         })

#     new_user = crud.create_user(db, user)
#     return {
#         "message": "Account successfully created",
#         "user": {
#             "user_id": new_user.user_id,
#             "nickname": new_user.nickname
#         }
#     }
@router.post("/signup", response_model=schemas.UserResponse, responses={400: {"model": schemas.ErrorResponse}})
def signup(user: schemas.User, db: Session = Depends(dependicies.get_db)):
    try:
        user = schemas.User(**user.dict())  # Validate user data
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={
            "message": "Account creation failed",
            "cause": e.errors()
        })
    
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

# @router.get("/users/{user_id}", 
#             response_model=schemas.UserResponse, 
#             responses={401: {"model": schemas.ErrorResponse}})
# def get_user(request: Request, user_id: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(dependicies.get_db)):
#     auth_header: Optional[str] = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Basic "):
#         return HTTPException(status_code=401, detail={"message": "Authentication Failed"})

#     auth_header = auth_header[len("Basic "):]
#     try:
#         decoded_bytes = base64.b64decode(auth_header)
#         decoded_str = decoded_bytes.decode("utf-8")
#         auth_user_id, password = decoded_str.split(":", 1)
#         # user_id, password = decoded_str.split(":", 1)
#     except Exception as e:
#         raise HTTPException(status_code=401, detail={"message": "Authentication Failed"})

#     db_user = crud.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=401, detail={"message": "No User found"})
    
#     auth_user = crud.get_user(db, auth_user_id)
#     if not auth_user or auth_user.password != password:
#         raise HTTPException(status_code=401, detail={"message": "Authentication Failed"})

#     return {
#         "message": "User details by user_id",
#         "user": {
#             "user_id": db_user.user_id,
#             "nickname": db_user.nickname,
#         }
#     }
@router.get("/users/{user_id}", 
            response_model=schemas.UserResponse, 
            responses={401: {"model": schemas.ErrorResponse}})
def get_user(request: Request, user_id: str, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(dependicies.get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:  
        auth_user_id = credentials.username
        password = credentials.password

        # Perform authentication
        if not auth_user_id or not password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication credentials missing")
        
       
        # if not auth_header or not auth_header.startswith("Basic "):
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

        # Verify authentication credentials
        auth_user = crud.get_user(db, auth_user_id)
        if not auth_user or auth_user.password != password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

        # Get user details
        db_user = crud.get_user(db, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return {
            "message": "User details by user_id",
            "user": {
                "user_id": db_user.user_id,
                "nickname": db_user.nickname,
            }
        }
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return {"message": "Authentication Failed"}
        else:
            raise e  # Re-raise the exception if it's not a 401 error

@router.patch("/users/{user_id}", response_model=schemas.UserResponse, responses={404: {"model": schemas.ErrorResponse}})
def update_user(user_id: str, update: schemas.UpdateUser, db: Session = Depends(dependicies.get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail={
            "message": "User not found",
            "cause": "Invalid user_id"
        })

  
    updated_user = crud.update_user(db, user_id, update.nickname, update.comment)
    # if updated_user.comment:
    return {
        "message": "User successfully updated",
        "user": {
            "user_id": updated_user.user_id,
            "nickname": updated_user.nickname,
            "comment": updated_user.comment,
        }
    }
    # if not updated_user.comment:
    #     return {
    #         "message": "User successfully updated",
    #         "user": {
    #             "user_id": updated_user.user_id,
    #             "nickname": updated_user.nickname,
    #         }
    #     }


# @router.post("/close", response_model=schemas.DeleteUserResponse, responses={401: {"model": schemas.AuthErrorResponse}})
# def delete_user(request: Request, db: Session = Depends(dependicies.get_db)):
#     auth_header: Optional[str] = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Basic "):
#         raise HTTPException(status_code=401, detail={"message": "Authentication Failed"})

#     auth_header = auth_header[len("Basic "):]
#     try:
#         decoded_bytes = base64.b64decode(auth_header)
#         decoded_str = decoded_bytes.decode("utf-8")
#         user_id, password = decoded_str.split(":", 1)
#     except Exception as e:
#         raise HTTPException(status_code=401, detail={"message": "Authentication Failed"})

#     db_user = crud.get_user(db, user_id)
#     if not db_user or db_user.password != password:
#         raise HTTPException(status_code=401, detail={"message": "Invalid user_id or password"})

#     crud.delete_user(db, user_id)
#     return {"message": "Account and user successfully removed"}

# # User Verification Function
# def verification(creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(dependicies.get_db)):
#     user_id = creds.username
#     password = creds.password
#     db_user = crud.get_user(db, user_id)
#     if not db_user and db_user.password != password:
#         print("User Validated")
#         return True
#     else:
#         # From FastAPI 
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail={"message": "Authentication Failed"},
#             # headers={"WWW-Authenticate": "Basic"},
#         )

# @router.post("/close", response_model=schemas.DeleteUserResponse, responses={401: {"model": schemas.AuthErrorResponse}})
# def delete_user(request: Request,  credentials = Depends(verification), db: Session = Depends(dependicies.get_db)):
#     user_id = credentials.username.encode("utf-8")
#     password = credentials.password.encode("utf-8")

#     db_user = crud.get_user(db, user_id)
#     # if not db_user or db_user.password != password:
#     #     raise HTTPException(status_code=401, detail={"message": "Invalid user_id or password"})

#     crud.delete_user(db, user_id)
#     return {"message": "Account and user successfully removed"}



@router.post("/close", response_model=schemas.DeleteUserResponse, responses={401: {"model": schemas.AuthErrorResponse}})
def delete_user(request: Request, db: Session = Depends(dependicies.get_db), credentials: HTTPBasicCredentials = Depends(security)):
    user_id = credentials.username
    password = credentials.password

    db_user = crud.get_user(db, user_id)
    if not db_user or db_user.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Invalid user_id or password"})

    crud.delete_user(db, user_id)
    return {"message": "Account and user successfully removed"}