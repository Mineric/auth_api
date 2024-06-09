from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: str = Field(..., example="TaroYamada")
    password: str = Field(..., example="PaSSwd4TY")

class UpdateUser(BaseModel):
    nickname: str = Field(None, example="Taro")

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
