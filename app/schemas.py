from pydantic import BaseModel, validator, constr, Field
import re

class User(BaseModel):
    user_id: constr(min_length=6, max_length=20) = Field(None, example="TaroYamada")
    password: constr(min_length=8, max_length=20) = Field(None, example="PaSSwd4TY")
    nickname: str = Field(None, example="Taro")
    comment: str = Field(None, example="I am happy!")

class CreateUser(BaseModel):
    user_id: constr(min_length=6, max_length=20) = Field(None, example="TaroYamada")
    password: constr(min_length=8, max_length=20) = Field(None, example="PaSSwd4TY")
    # user_id: str = Field(None, example="TaroYamada")
    # password: str = Field(None, example="PaSSwd4TY")

    @validator('user_id')
    def user_id_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9]{6,20}$', v):
            raise ValueError("user_id must be 6-20 halfwidth alphanumeric characters.")
        return v

    @validator('password')
    def password_valid(cls, v):
        if not re.match(r'^[\x21-\x7E]{8,20}$', v):  # \x21 to \x7E are printable ASCII characters excluding space
            raise ValueError("password must be 8-20 ASCII characters without spaces or control characters.")
        return v
    
class UpdateUser(BaseModel):
    nickname: str = Field(None, example="Taro")
    comment: str = Field(None, example="I am happy!")

class UpdateUserResponse(BaseModel):
    message: str
    recipe: list
    # nickname: str = Field(None, example="Taro")
    # comment: str = Field(None, example="I am happy!")

class UserResponse(BaseModel):
    message: str
    user: dict

class ErrorResponse(BaseModel):
    message: str
    cause: str

class DeleteUserResponse(BaseModel):
    message: str

class AuthErrorResponse(BaseModel):
    message: str

# from pydantic import BaseModel, constr, Field, validator

# class User(BaseModel):
#     user_id: constr(min_length=6, max_length=20) = Field(..., example="TaroYamada")
#     password: constr(min_length=8, max_length=20) = Field(..., example="PaSSwd4TY")
#     nickname: str = Field(None, example="Taro")
#     comment: str = Field(None, example="I am happy!")

# class CreateUser(BaseModel):
#     user_id: constr(min_length=6, max_length=20) = Field(..., example="TaroYamada")
#     password: constr(min_length=8, max_length=20) = Field(..., example="PaSSwd4TY")

#     @validator('user_id')
#     def validate_user_id(cls, v):
#         if not v:
#             raise ValueError("required user_id")
#         return v

#     @validator('password')
#     def validate_password(cls, v):
#         if not v:
#             raise ValueError("required password")
#         return v

# class UpdateUser(BaseModel):
#     nickname: str = Field(None, example="Taro")
#     comment: str = Field(None, example="I am happy!")

# class UpdateUserResponse(BaseModel):
#     message: str
#     recipe: list

# class UserResponse(BaseModel):
#     message: str
#     user: dict

# class ErrorResponse(BaseModel):
#     message: str
#     cause: str

# class DeleteUserResponse(BaseModel):
#     message: str

# class AuthErrorResponse(BaseModel):
#     message: str
