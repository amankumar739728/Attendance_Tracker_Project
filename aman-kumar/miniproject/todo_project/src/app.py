import argparse
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from api.routes import router as task_router
from api.library_router import router as library_router
from core.auth import authenticate_user, create_access_token,create_refresh_token
from middleware.auth_middleware import AuthMiddleware
from models.schema import LoginRequest

app = FastAPI()



@app.post("/login", tags=["Auth"])
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000, help="Port to run the app on")
args = parser.parse_args()

app.include_router(task_router)
app.include_router(library_router)
app.add_middleware(AuthMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(args.port))
    
    
# C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025>cd workarea\aman-kumar\miniproject\todo_project

# C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025\workarea\aman-kumar\miniproject\todo_project>venv\Scripts\activate

# (venv) C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025\workarea\aman-kumar\miniproject\todo_project>python src/app.py --port=9123