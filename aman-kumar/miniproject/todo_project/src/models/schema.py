from pydantic import BaseModel


class SampleResponse(BaseModel):
    message: str
    status: str    

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    
class LoginRequest(BaseModel):
    username: str = "aman"
    password: str = "test"
