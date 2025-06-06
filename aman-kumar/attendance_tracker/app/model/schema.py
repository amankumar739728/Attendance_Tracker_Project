from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import datetime

class CreateUserRequest(BaseModel):
    emp_id: str = "1398"
    username: str = "aman"
    email: str = "test@gmail.com"
    password: str = "test"
    department: str = "Microsoft & Open Source"
    sub_department: str = "Application Development"
    is_admin: bool = False

class LoginRequest(BaseModel):
    username: str = "aman"
    password: str = "Test@1234"
    
class LoginRequestRoot(BaseModel):
    username: str = "root"
    password: str = "password"
    
    
class UserOut(BaseModel):
    emp_id: str
    username: str
    email: str
    department: str
    sub_department: str
    is_admin: bool

    class Config:
        from_attributes = True

class UpdateUserRequest(BaseModel):
    emp_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    department: Optional[str] = None
    sub_department: Optional[str] = None
    is_admin: Optional[bool] = None

class AccessLogIn(BaseModel):
    action: str ="IN" # 'IN' or 'OUT'

class AccessLogUpdate(BaseModel):
    action: str
    timestamp: datetime

class AccessLogOut(BaseModel):
    id: int
    user_id: int
    emp_id: str
    timestamp: datetime  # changed from str to datetime
    action: str
    class Config:
        from_attributes = True

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
            
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# Model for Reset Password request
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
class ChatbotRequest(BaseModel):
    message: str
    
class ChatbotResponse(BaseModel):
    response: str
    options: List[str] = []
