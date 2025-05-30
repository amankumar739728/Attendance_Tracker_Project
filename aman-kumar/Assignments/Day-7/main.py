import argparse
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from user_crud_model import authenticate_user, create_user, get_user, get_all_users, update_user_password, delete_user
from auth import create_access_token, create_refresh_token, get_current_user
from fastapi import HTTPException, Depends,Query

from security import AuthMiddleware
from schema import LoginRequest, UserUpdateRequest

app = FastAPI()

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000, help="Port to run the app on")
args = parser.parse_args()

@app.post("/login", tags=["Auth"])
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": request.username})
    refresh_token = create_refresh_token(data={"sub": request.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/register", tags=["Auth"])
def register(request: LoginRequest):
    success = create_user(request.username, request.password)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}

@app.get("/user/me", tags=["User"])
def read_user(current_user: dict = Depends(get_current_user)):
    return {"id": current_user["id"], "username": current_user["username"]}

@app.put("/user/me", tags=["User"])
def update_user(request: UserUpdateRequest, current_user: dict = Depends(get_current_user)):
    # For simplicity, only allow password update
    success = update_user_password(current_user["username"], request.password)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update password")
    return {"message": "User password updated successfully"}

@app.delete("/user/me", tags=["User"])
def delete_current_user(current_user: dict = Depends(get_current_user)):
    success = delete_user(current_user["username"])
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete user")
    return {"message": "User deleted successfully"}

@app.get("/users/all", tags=["User"])
def read_all_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), current_user: dict = Depends(get_current_user)):
    users = get_all_users(skip=skip, limit=limit)
    return {"users": users}

@app.get("/users/{username}", tags=["User"])
def read_user_by_username(username: str, current_user: dict = Depends(get_current_user)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user["id"], "username": user["username"]}

@app.put("/users/update-password/{username}", tags=["User"])
def update_password_for_user(username: str, request: UserUpdateRequest, current_user: dict = Depends(get_current_user)):
    success = update_user_password(username, request.password)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update password")
    return {"message": "User password updated successfully"}

@app.delete("/users/delete/{username}", tags=["User"])
def delete_user_by_username(username: str, current_user: dict = Depends(get_current_user)):
    success = delete_user(username)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete user")
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(args.port))
