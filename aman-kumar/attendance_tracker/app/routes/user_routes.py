from fastapi import (APIRouter, Depends, HTTPException, status,BackgroundTasks)
from fastapi.security import OAuth2PasswordBearer
from configs.auth import login_user, authenticate_user, create_access_token, create_refresh_token, verify_refresh_token
from model.crud import get_all_users, get_user_by_username, create_user, update_user, delete_user
from model.models import User, AccessLog, ResetToken
from configs.database import db_session
from typing import List
from pydantic import BaseModel
from fastapi.security import HTTPBearer
from model.schema import (CreateUserRequest,LoginRequest, LoginRequestRoot, UpdateUserRequest, UserOut, AccessLogIn, AccessLogOut,AccessLogUpdate,TokenRefreshRequest,TokenRefreshResponse,ChangePasswordRequest,ForgotPasswordRequest,ResetPasswordRequest,ChatbotRequest,ChatbotResponse)
from datetime import datetime, date, timedelta
from fastapi import Body, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from configs.logging_config import logger
from configs.config import settings
from utils.jwt_utils import decode_token
from configs.auth import hash_password,verify_password, validate_password_complexity
from model.reset_password_email import send_reset_email
import secrets
import asyncio


router = APIRouter(prefix="/v1/user")

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme = HTTPBearer()


def get_current_user(token: str = Depends(oauth2_scheme)):
    data = decode_token(token.credentials)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db_session.query(User).filter_by(username=data["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user

def send_reset_email_background(email: str, token: str):
    asyncio.create_task(send_reset_email(email, token))

@router.post("/chatbot/message", response_model=ChatbotResponse, tags=["Chatbot"])
def chatbot_message(request: ChatbotRequest, current_user: User = Depends(get_current_user)):
    user_message = request.message.strip().lower()
    username = current_user.username
    emp_id = current_user.emp_id

    # Basic greeting
    if user_message in ["hi", "hello", "hey"]:
        return ChatbotResponse(
            response=f"Hello {username}! How can I assist you with your attendance today?",
            options=["Show attendance for today", "Show attendance for a particular day"]
        )
    # Who am I query
    elif "who am i" in user_message:
        return ChatbotResponse(
            response=f"You are {username}, employee ID {emp_id}. How can I help you?",
            options=["Back"]
        )
    # Attendance query
    elif "attendance" in user_message:
        return ChatbotResponse(
            response="Please choose an option:",
            options=["Show attendance for today", "Show attendance for a particular day"]
        )
    # Handle option selection
    elif user_message == "show attendance for today":
        # Fetch today's attendance for the user
        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        logs = db_session.query(AccessLog).filter(
            AccessLog.emp_id == emp_id,
            AccessLog.timestamp.between(f"{today_str} 00:00:00", f"{today_str} 23:59:59")
        ).order_by(AccessLog.timestamp).all()
        if not logs:
            return ChatbotResponse(response="No attendance records found for today.", options=[])
        response_lines = [f"Attendance records for today ({today_str}):"]
        for log in logs:
            time_str = log.timestamp.strftime("%H:%M:%S")
            response_lines.append(f"{log.action} at {time_str}")
        return ChatbotResponse(response="\n".join(response_lines), options=[])
    elif user_message == "show attendance for a particular day":
        return ChatbotResponse(
            response="Please enter the date in YYYY-MM-DD format.",
            options=[]
        )
    else:
        return ChatbotResponse(
            response="Sorry, I didn't understand that. You can say 'Hi', ask 'Who am I', or ask about your attendance.",
            options=[]
        )

@router.post("/register", status_code=status.HTTP_201_CREATED,tags=["Auth"])
def register(request: CreateUserRequest):
    data = request.dict()
    try:
        logger.info(f"Register attempt for email: {data['email']}")
        if db_session.query(User).filter_by(email=data["email"]).first():
            logger.warning(f"Registration failed: Email already exists - {data['email']}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        user = create_user(db_session, data)
        if not user:
            logger.error(f"User registration failed for email: {data['email']}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User registration failed")
        logger.info(f"User registered successfully: {user.username}")
        return {"message": f"User '{user.username}' registered successfully"}
    except IntegrityError:
        db_session.rollback()
        logger.error(f"Integrity error during registration for email: {data['email']}")
        raise HTTPException(status_code=400, detail="Integrity error: possible duplicate or constraint violation")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Database error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except TypeError as e:
        logger.error(f"Type error during registration: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Type error: {str(e)}")
    except AttributeError as e:
        logger.error(f"Attribute error during registration: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Attribute error: {str(e)}")
    except HTTPException as e:
        logger.warning(f"HTTPException during registration: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/login",status_code=status.HTTP_200_OK,tags=["Auth"])
def login(request: LoginRequest):
    try:
        logger.info(f"Login attempt for username: {request.username}")
        tokens = login_user(request.username, request.password)
        if not tokens:
            logger.warning(f"Login failed for username: {request.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        logger.info(f"Login successful for username: {request.username}")
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer"
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except TypeError as e:
        logger.error(f"Type error during login: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Type error: {str(e)}")
    except AttributeError as e:
        logger.error(f"Attribute error during login: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Attribute error: {str(e)}")
    except HTTPException as e:
        logger.warning(f"HTTPException during login: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/login2", status_code=status.HTTP_200_OK,tags=["Auth"])
def login(request: LoginRequestRoot):
    try:
        logger.info(f"Login2 attempt for username: {request.username}")
        user = authenticate_user(request.username, request.password)
        if not user:
            logger.warning(f"Login2 failed for username: {request.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": request.username})
        refresh_token = create_refresh_token(data={"sub": request.username})
        logger.info(f"Login2 successful for username: {request.username}")
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except SQLAlchemyError as e:
        logger.error(f"Database error during login2: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except TypeError as e:
        logger.error(f"Type error during login2: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Type error: {str(e)}")
    except AttributeError as e:
        logger.error(f"Attribute error during login2: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Attribute error: {str(e)}")
    except HTTPException as e:
        logger.warning(f"HTTPException during login2: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login2: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
@router.post("/refresh-token", response_model=TokenRefreshResponse,tags=["Auth"])
async def refresh_token(request: TokenRefreshRequest):
    try:
        # Verify the refresh token
        payload = verify_refresh_token(request.refresh_token)
        # Create new access token
        access_token = create_access_token(
            data={"sub": payload["sub"]},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
        
@router.post("/forgot-password", tags=["Auth"])
def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    user = db_session.query(User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)

    token_entry = ResetToken(email=user.email, token=reset_token, expires_at=expiry)
    db_session.add(token_entry)
    db_session.commit()

    background_tasks.add_task(send_reset_email_background, user.email, reset_token)

    return {
        "message": f"Password reset link sent to your email: {user.email}",
        "reset_link": f"https://attendance-tracker-project-ui.onrender.com/#/reset-password?token={reset_token}"
    }
    
@router.post("/reset-password", tags=["Auth"])
def reset_password(request: ResetPasswordRequest):
    token_entry = db_session.query(ResetToken).filter_by(token=request.token).first()
    if not token_entry or token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if not request.new_password:
        raise HTTPException(status_code=400, detail="New password is required")
    is_valid, msg = validate_password_complexity(request.new_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    user = db_session.query(User).filter_by(email=token_entry.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(request.new_password)
    db_session.commit()

    db_session.delete(token_entry)
    db_session.commit()

    return {"message": "Password has been reset successfully"}


@router.get("/current-user", response_model=UserOut,tags=["UserManagement"])
def read_current_user(current_user: User = Depends(get_current_user)):
    try:
        return {
            "emp_id": current_user.emp_id,
            "username": current_user.username,
            "email": current_user.email,
            "department": current_user.department,
            "sub_department": current_user.sub_department,
            "is_admin": current_user.is_admin
        }
    except AttributeError as e:
        raise HTTPException(status_code=400, detail=f"Attribute error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# User Management Routes

@router.get("/all", response_model=List[UserOut],tags=["UserManagement"])
def read_users(current_user: User = Depends(admin_required)):
    try:
        users = get_all_users(db_session)
        return [
            {
                "emp_id": user.emp_id,
                "username": user.username,
                "email": user.email,
                "department": user.department,
                "sub_department": user.sub_department,
                "is_admin": user.is_admin
            }
            for user in users
        ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/users/{username}", response_model=UserOut,tags=["UserManagement"])
def read_user(username: str, current_user: User = Depends(admin_required)):
    try:
        user = get_user_by_username(db_session, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {
            "emp_id": user.emp_id,
            "username": user.username,
            "email": user.email,
            "department": user.department,
            "sub_department": user.sub_department,
            "is_admin": user.is_admin
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
@router.get("/users/by-emp_id/{emp_id}", response_model=UserOut, tags=["UserManagement"])
def read_user_by_emp_id(emp_id: str, current_user: User = Depends(admin_required)):
    try:
        user = db_session.query(User).filter_by(emp_id=emp_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {
            "emp_id": user.emp_id,
            "username": user.username,
            "email": user.email,
            "department": user.department,
            "sub_department": user.sub_department,
            "is_admin": user.is_admin
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.put("/users/{username}", response_model=UserOut,tags=["UserManagement"])
def update_user_details(username: str, updated_data: UpdateUserRequest, current_user: User = Depends(get_current_user)):
    # Allow if admin or user is updating their own profile
    if not (current_user.is_admin or current_user.username == username):
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")
    try:
        if username == "root":
            raise HTTPException(status_code=403, detail="Root user details cannot be updated")
        user = update_user(db_session, current_user, username, updated_data.dict(exclude_unset=True))
        return user
    except SQLAlchemyError as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/users/{username}",tags=["UserManagement"])
def delete_user_route(username: str, current_user: User = Depends(admin_required)):
    try:
        if username == "root":
            raise HTTPException(status_code=403, detail="Root user cannot be deleted")
        result = delete_user(db_session, current_user, username)
        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
@router.post("/change-password", tags=["UserManagement"])
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        user = db_session.query(User).filter(User.username == current_user.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check current password
        if not verify_password(request.current_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        # Check new password confirmation
        if request.new_password != request.confirm_password:
            raise HTTPException(status_code=400, detail="New password and confirm password do not match")

        # Check new password complexity
        is_valid, msg = validate_password_complexity(request.new_password)
        if not is_valid:
            raise HTTPException(status_code=400, detail=msg)

        # Ensure new password is different
        if verify_password(request.new_password, user.password_hash):
            raise HTTPException(status_code=400, detail="New password must be different from current password")

        # Update password
        user.password_hash = hash_password(request.new_password)
        db_session.commit()

        return {"success": True, "message": "Password changed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Attendance Tracker Routes

@router.post("/attendance/punch", tags=["Attendance Tracker"])
def punch_attendance(
    log: AccessLogIn = Body(...),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Attendance punch attempt for user: {current_user.username}, action: {log.action}")
        if log.action not in ["IN", "OUT"]:
            logger.warning(f"Invalid punch action: {log.action} by user: {current_user.username}")
            raise HTTPException(status_code=400, detail="Action must be 'IN' or 'OUT'")
        access_log = AccessLog(user_id=current_user.id,emp_id=current_user.emp_id, action=log.action, timestamp=datetime.utcnow())
        db_session.add(access_log)
        db_session.commit()
        db_session.refresh(access_log)
        logger.info(f"Attendance punch successful for user: {current_user.username}, action: {log.action}")
        def add_5hr_30min(dt):
            if not dt:
                return None
            dt_added = dt + timedelta(hours=5, minutes=30)
            return dt_added.strftime("%Y-%m-%d %H:%M:%S")
        access_log_out = AccessLogOut.from_orm(access_log)
        result = access_log_out.dict()
        result["timestamp_ist"] = add_5hr_30min(access_log_out.timestamp)
        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Database error during attendance punch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        logger.warning(f"HTTPException during attendance punch: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during attendance punch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

from zoneinfo import ZoneInfo

@router.get("/attendance/daily-summary", tags=["Attendance Tracker"])
def get_daily_attendance_summary(
    emp_id: str = None,
    summary_date: str = None,
    current_user: User = Depends(get_current_user)
):
    ist = ZoneInfo("Asia/Kolkata")
    # Admin can view all users' summary, normal users only their own
    if not emp_id:
        if current_user.is_admin:
            # Return summary for all users
            users = db_session.query(User).all()
            summaries = []
            for user in users:
                logs = db_session.query(AccessLog).filter(
                    AccessLog.user_id == user.id,
                    AccessLog.timestamp.between(
                        datetime.combine(date.today() if not summary_date else datetime.strptime(summary_date, "%Y-%m-%d").date(), datetime.min.time()),
                        datetime.combine(date.today() if not summary_date else datetime.strptime(summary_date, "%Y-%m-%d").date(), datetime.max.time())
                    )
                ).order_by(AccessLog.timestamp).all()
                first_in = next((l.timestamp for l in logs if l.action == "IN"), None)
                last_out = next((l.timestamp for l in reversed(logs) if l.action == "OUT"), None)
                # Add 5 hours 30 minutes to the time (do not use timezone conversion)
                def add_5hr_30min(dt):
                    if not dt:
                        return None
                    dt_added = dt + timedelta(hours=5, minutes=30)
                    return dt_added.strftime("%Y-%m-%d %H:%M:%S")
                first_in_str = add_5hr_30min(first_in) if first_in else None
                last_out_str = add_5hr_30min(last_out) if last_out else None
                all_logs_ist = []
                for l in logs:
                    log_ist = AccessLogOut.from_orm(l)
                    log_dict = log_ist.dict()
                    log_dict["timestamp_ist"] = add_5hr_30min(log_ist.timestamp)
                    all_logs_ist.append(log_dict)
                summaries.append({
                    "user_id": user.id,
                    "emp_id": user.emp_id,
                    "username": user.username,
                    "department": user.department,
                    "sub_department": user.sub_department,
                    "first_in": first_in_str,
                    "last_out": last_out_str,
                    "all_logs": all_logs_ist
                })
            return summaries
        else:
            emp_id = current_user.emp_id
    else:
        if not current_user.is_admin and emp_id != current_user.emp_id:
            raise HTTPException(status_code=403, detail="Not authorized")
    # Single user summary
    user = db_session.query(User).filter(User.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user.id
    try:
        summary_date_obj = datetime.strptime(summary_date, "%Y-%m-%d").date() if summary_date else date.today()
    except ValueError:
        raise HTTPException(status_code=400, detail="Date format must be YYYY-MM-DD (e.g., 2025-05-21)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date: {str(e)}")
    try:
        logs = db_session.query(AccessLog).filter(
            AccessLog.user_id == user_id,
            AccessLog.timestamp.between(
                datetime.combine(summary_date_obj, datetime.min.time()),
                datetime.combine(summary_date_obj, datetime.max.time())
            )
        ).order_by(AccessLog.timestamp).all()
        if not logs:
            # Always return user details even if no logs
            return {
                "message": "No attendance records found for this date.",
                "emp_id": user.emp_id,
                "username": user.username,
                "department": user.department,
                "sub_department": user.sub_department
            }
        first_in = next((l.timestamp for l in logs if l.action == "IN"), None)
        last_out = next((l.timestamp for l in reversed(logs) if l.action == "OUT"), None)
        # Add 5 hours 30 minutes to the time (do not use timezone conversion)
        def add_5hr_30min(dt):
            if not dt:
                return None
            dt_added = dt + timedelta(hours=5, minutes=30)
            return dt_added.strftime("%Y-%m-%d %H:%M:%S")
        first_in_str = add_5hr_30min(first_in) if first_in else None
        last_out_str = add_5hr_30min(last_out) if last_out else None
        all_logs_ist = []
        for l in logs:
            log_ist = AccessLogOut.from_orm(l)
            log_dict = log_ist.dict()
            log_dict["timestamp_ist"] = add_5hr_30min(log_ist.timestamp)
            all_logs_ist.append(log_dict)
        return {
            "date": summary_date_obj.isoformat(),
            "emp_id": user.emp_id,
            "username": user.username,
            "department": user.department,  # <-- add department
            "sub_department": user.sub_department,  # <-- add sub_department
            "first_in": first_in_str,
            "last_out": last_out_str,
            "all_logs": all_logs_ist
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/attendance/by-emp_id", tags=["Attendance Tracker"])
def get_attendance_by_emp_id(emp_id: str, date_str: str = Query(...), current_user: User = Depends(get_current_user)):
    # Restrict non-admins to only their own emp_id
    if not current_user.is_admin and emp_id != current_user.emp_id:
        return {"message": "Access restricted: only your own attendance details can be viewed."}
    try:
        summary_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Date format must be YYYY-MM-DD (e.g., 2025-05-21)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date: {str(e)}")
    try:
        user = db_session.query(User).filter(User.emp_id == emp_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        logs = db_session.query(AccessLog).filter(
            AccessLog.user_id == user.id,
            AccessLog.timestamp.between(
                datetime.combine(summary_date_obj, datetime.min.time()),
                datetime.combine(summary_date_obj, datetime.max.time())
            )
        ).order_by(AccessLog.timestamp).all()
        def add_5hr_30min(dt):
            if not dt:
                return None
            dt_added = dt + timedelta(hours=5, minutes=30)
            return dt_added.strftime("%Y-%m-%d %H:%M:%S")
        if not logs:
            # Always return user details even if no logs
            return {
                "message": "No attendance records found for this date.",
                "emp_id": user.emp_id,
                "username": user.username,
                "department": user.department,
                "sub_department": user.sub_department
            }
        first_in = next((l.timestamp for l in logs if l.action == "IN"), None)
        last_out = next((l.timestamp for l in reversed(logs) if l.action == "OUT"), None)
        first_in_str = add_5hr_30min(first_in) if first_in else None
        last_out_str = add_5hr_30min(last_out) if last_out else None
        all_logs_ist = []
        for l in logs:
            log_ist = AccessLogOut.from_orm(l)
            log_dict = log_ist.dict()
            log_dict["timestamp_ist"] = add_5hr_30min(log_ist.timestamp)
            all_logs_ist.append(log_dict)
        # Always return user details, even if no logs
        result = {
            "date": summary_date_obj.isoformat(),
            "emp_id": user.emp_id,
            "username": user.username,
            "department": user.department,
            "sub_department": user.sub_department,
            "first_in": first_in_str,
            "last_out": last_out_str,
            "all_logs": all_logs_ist
        }
        if not logs:
            result["message"] = "No attendance records found for this date."
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/attendance/by-username", tags=["Attendance Tracker"])
def get_attendance_by_username(username: str, date_str: str = Query(...), current_user: User = Depends(get_current_user)):
    # Restrict non-admins to only their own username
    if not current_user.is_admin and username != current_user.username:
        return {"message": "Access restricted: only your own attendance details can be viewed."}
    try:
        summary_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Date format must be YYYY-MM-DD (e.g., 2025-05-21)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date: {str(e)}")
    try:
        user = db_session.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        logs = db_session.query(AccessLog).filter(
            AccessLog.user_id == user.id,
            AccessLog.timestamp.between(
                datetime.combine(summary_date_obj, datetime.min.time()),
                datetime.combine(summary_date_obj, datetime.max.time())
            )
        ).order_by(AccessLog.timestamp).all()
        def add_5hr_30min(dt):
            if not dt:
                return None
            dt_added = dt + timedelta(hours=5, minutes=30)
            return dt_added.strftime("%Y-%m-%d %H:%M:%S")
        if not logs:
            # Always return user details even if no logs
            return {
                "message": "No attendance records found for this date.",
                "emp_id": user.emp_id,
                "username": user.username,
                "department": user.department,
                "sub_department": user.sub_department
            }
        first_in = next((l.timestamp for l in logs if l.action == "IN"), None)
        last_out = next((l.timestamp for l in reversed(logs) if l.action == "OUT"), None)
        first_in_str = add_5hr_30min(first_in) if first_in else None
        last_out_str = add_5hr_30min(last_out) if last_out else None
        all_logs_ist = []
        for l in logs:
            log_ist = AccessLogOut.from_orm(l)
            log_dict = log_ist.dict()
            log_dict["timestamp_ist"] = add_5hr_30min(log_ist.timestamp)
            all_logs_ist.append(log_dict)
        # Always return user details, even if no logs
        result = {
            "date": summary_date_obj.isoformat(),
            "emp_id": user.emp_id,
            "username": user.username,
            "department": user.department,
            "sub_department": user.sub_department,
            "first_in": first_in_str,
            "last_out": last_out_str,
            "all_logs": all_logs_ist
        }
        if not logs:
            result["message"] = "No attendance records found for this date."
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
@router.delete("/attendance/delete", tags=["Attendance Tracker"])
def delete_attendance_by_emp_id(emp_id: str = Query(...), current_user: User = Depends(admin_required)):
    """
    Delete all attendance logs for a given emp_id. Only admin can perform this action.
    Restrict deletion if emp_id is 'root001'.
    """
    try:
        if emp_id == "root001":
            raise HTTPException(status_code=403, detail="Cannot delete logs for root admin user.")
        user = db_session.query(User).filter(User.emp_id == emp_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Delete all logs for this user
        db_session.query(AccessLog).filter(AccessLog.user_id == user.id).delete()
        db_session.commit()
        logger.info(f"All attendance logs deleted for emp_id: {emp_id} by admin: {current_user.username}")
        return {"message": f"All attendance logs deleted for emp_id: {emp_id}"}
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Database error during attendance delete: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        logger.warning(f"HTTPException during attendance delete: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during attendance delete: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/attendance/delete_by_day", tags=["Attendance Tracker"])
def delete_attendance_by_emp_id_and_day(emp_id: str = Query(...), date_str: str = Query(...), current_user: User = Depends(admin_required)):
    """
    Delete attendance logs for a given emp_id on a specific day. Only admin can perform this action.
    Restrict deletion if emp_id is 'root001'.
    """
    try:
        if emp_id == "root001":
            raise HTTPException(status_code=403, detail="Cannot delete logs for root admin user.")
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Date format must be YYYY-MM-DD (e.g., 2025-05-21)")
        user = db_session.query(User).filter(User.emp_id == emp_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        deleted_count = db_session.query(AccessLog).filter(
            AccessLog.user_id == user.id,
            AccessLog.timestamp.between(start_datetime, end_datetime)
        ).delete(synchronize_session=False)
        db_session.commit()
        logger.info(f"Attendance logs deleted for emp_id: {emp_id} on {date_str} by admin: {current_user.username}")
        return {"message": f"Deleted {deleted_count} attendance logs for emp_id: {emp_id} on {date_str}"}
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Database error during attendance delete by day: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        logger.warning(f"HTTPException during attendance delete by day: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during attendance delete by day: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# @router.put("/attendance/update_by_day", tags=["Attendance Tracker"])
# def update_attendance_by_emp_id_and_day(
#     emp_id: str = Query(...),
#     date_str: str = Query(...),
#     updated_logs: List[AccessLogIn] = Body(...),
#     current_user: User = Depends(admin_required)
# ):
#     """
#     Update attendance logs for a given emp_id on a specific day. Only admin can perform this action.
#     """
#     try:
#         if emp_id == "root001":
#             raise HTTPException(status_code=403, detail="Cannot update logs for root admin user.")
#         try:
#             breakpoint()
#             target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Date format must be YYYY-MM-DD (e.g., 2025-05-21)")
#         user = db_session.query(User).filter(User.emp_id == emp_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         start_datetime = datetime.combine(target_date, datetime.min.time())
#         end_datetime = datetime.combine(target_date, datetime.max.time())
#         # Fetch existing logs for the day
#         existing_logs = db_session.query(AccessLog).filter(
#             AccessLog.user_id == user.id,
#             AccessLog.timestamp.between(start_datetime, end_datetime)
#         ).all()
#         # Update existing logs or add new ones if needed
#         for updated_log in updated_logs:
#             # Find matching log by id or timestamp and action
#             matched_log = next((log for log in existing_logs if log.id == updated_log.id), None)
#             if matched_log:
#                 matched_log.action = updated_log.action
#                 matched_log.timestamp = updated_log.timestamp
#             else:
#                 # Add new log
#                 new_log = AccessLog(
#                     user_id=user.id,
#                     emp_id=user.emp_id,
#                     action=updated_log.action,
#                     timestamp=updated_log.timestamp
#                 )
#                 db_session.add(new_log)
#         db_session.commit()
#         return {"message": f"Attendance logs updated for emp_id: {emp_id} on {date_str}"}
#     except SQLAlchemyError as e:
#         db_session.rollback()
#         logger.error(f"Database error during attendance update by day: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
#     except HTTPException as e:
#         logger.warning(f"HTTPException during attendance update by day: {str(e)}")
#         raise e
#     except Exception as e:
#         logger.error(f"Unexpected error during attendance update by day: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
# @router.put("/attendance/update_by_day", tags=["Attendance Tracker"])
# def update_attendance_by_emp_id_and_day(
#     emp_id: str = Query(...),
#     date_str: str = Query(...),
#     updated_logs: List[AccessLogUpdate] = Body(...),
#     current_user: User = Depends(admin_required)
# ):
#     try:
#         if emp_id == "root001":
#             raise HTTPException(status_code=403, detail="Cannot update logs for root admin user.")

#         try:
#             target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Date format must be YYYY-MM-DD (e.g., 2025-05-21)")

#         user = db_session.query(User).filter(User.emp_id == emp_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         start_datetime = datetime.combine(target_date, datetime.min.time())
#         end_datetime = datetime.combine(target_date, datetime.max.time())

#         existing_logs = db_session.query(AccessLog).filter(
#             AccessLog.user_id == user.id,
#             AccessLog.timestamp.between(start_datetime, end_datetime)
#         ).all()

#         # Log the intent
#         logger.info(f"Admin '{current_user.username}' is updating attendance for emp_id '{emp_id}' on '{date_str}' with {len(updated_logs)} log(s)")

#         updated_count = 0
#         added_count = 0

#         for updated_log in updated_logs:
#             matched_log = next((log for log in existing_logs if log.id == updated_log.id), None)
#             if matched_log:
#                 matched_log.action = updated_log.action
#                 matched_log.timestamp = updated_log.timestamp
#                 updated_count += 1
#             else:
#                 new_log = AccessLog(
#                     user_id=user.id,
#                     emp_id=user.emp_id,
#                     action=updated_log.action,
#                     timestamp=updated_log.timestamp
#                 )
#                 db_session.add(new_log)
#                 added_count += 1

#         db_session.commit()

#         logger.info(
#             f"Update by '{current_user.username}' complete: {updated_count} log(s) updated, {added_count} added "
#             f"for emp_id '{emp_id}' on '{date_str}' at {datetime.utcnow().isoformat()}."
#         )

#         return {
#             "message": f"Attendance logs updated for emp_id: {emp_id} on {date_str}",
#             "updated": updated_count,
#             "added": added_count
#         }

#     except SQLAlchemyError as e:
#         db_session.rollback()
#         logger.error(f"DB error by '{current_user.username}' while updating attendance: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#     except HTTPException as e:
#         logger.warning(f"HTTP error by '{current_user.username}': {str(e.detail)}")
#         raise e

#     except Exception as e:
#         logger.error(f"Unexpected error by '{current_user.username}': {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")





