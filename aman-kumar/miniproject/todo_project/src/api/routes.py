import traceback
from fastapi import APIRouter, Depends, HTTPException,Request
from core.auth import get_current_user
from models.store import user_tasks, fake_users_db
from core.security import hash_password
from models.schema import TokenRefreshRequest, TokenRefreshResponse
from core.auth import verify_refresh_token, create_access_token
from config import settings
from config.constants import Constants
from datetime import timedelta
from fastapi.responses import JSONResponse
from models.servicename import Mainclass



router = APIRouter()

@router.post("/refresh-token", response_model=TokenRefreshResponse, tags=["Auth"])
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
        
@router.get("/v1/sample/response/{fullname}", tags=["Sample"])
async def sample_endpoint(request: Request,fullname:str,current_user: dict = Depends(get_current_user)):
    if not fullname:
        raise HTTPException(status_code=400, detail="Please provide a name")
    # Log the incoming request
    print(f"Received request for fullname: {fullname}")
    print(f"Request headers: {request.headers}")
    data={}
    data[Constants.NAME] = fullname
    res= Mainclass(request, None)
    try:
        resp = await res.get_sample_response(data)
        if isinstance(resp, dict):  # Ensure it's a dict before using JSONResponse
            print("Returning successful response")
            return JSONResponse(content=resp, media_type="application/json", status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Invalid response format")
    
    except Exception as e:
        print(f"Error in sample_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/tasks/add", tags=["Task"])
def add_task(task: str, user: dict = Depends(get_current_user)):
    username = user["username"]
    if not task:
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    if username not in user_tasks:
        user_tasks[username] = []
    if task in user_tasks[username]:
        raise HTTPException(status_code=400, detail="Task already exists")
    # Add the task to the user's task list
    user_tasks[username].append(task)
    return {"msg": "Task added", "tasks": user_tasks[username]}

@router.delete("/tasks/remove", tags=["Task"])
def remove_task(task: str, user: dict = Depends(get_current_user)):
    username = user["username"]
    if task in user_tasks.get(username, []):
        user_tasks[username].remove(task)
        return {"msg": "Task removed", "tasks": user_tasks[username]}
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks", tags=["Task"])
def list_tasks(user: dict = Depends(get_current_user)):
    username = user["username"]
    return {"tasks": user_tasks.get(username, [])}

# User management endpoints

@router.get("/users", tags=["User"])
def list_users(user: dict = Depends(get_current_user)):
    return {"users": list(fake_users_db.keys())}

@router.get("/users/{username}", tags=["User"])
def get_user(username: str, user: dict = Depends(get_current_user)):
    user_data = fake_users_db.get(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user_data}

@router.post("/users/add", tags=["User"])
def add_user(username: str, password: str, user: dict = Depends(get_current_user)):
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password cannot be empty")
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hash_password(password)
    }
    user_tasks[username] = []
    return {"msg": "User added", "users": list(fake_users_db.keys())}

@router.put("/users/update", tags=["User"])
def update_user(old_username: str, new_username: str = None, new_password: str = None, user: dict = Depends(get_current_user)):
    if old_username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if new_username and new_username != old_username:
        if new_username in fake_users_db:
            raise HTTPException(status_code=400, detail="New username already exists")
        fake_users_db[new_username] = fake_users_db.pop(old_username)
        fake_users_db[new_username]["username"] = new_username
        user_tasks[new_username] = user_tasks.pop(old_username)
    if new_password:
        target_user = new_username if new_username else old_username
        fake_users_db[target_user]["hashed_password"] = hash_password(new_password)
    return {"msg": "User updated", "users": list(fake_users_db.keys())}

@router.delete("/users/remove", tags=["User"])
def remove_user(username: str, user: dict = Depends(get_current_user)):
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    fake_users_db.pop(username)
    user_tasks.pop(username, None)
    return {"msg": "User removed", "users": list(fake_users_db.keys())}