from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str = "aman"
    password: str = "test"


class UserUpdateRequest(BaseModel):
    password: str
    
class TokenData(BaseModel):
    username: str | None = None
