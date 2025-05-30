import argparse
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import user_routes
from configs.database import db_session, engine
from model.models import User, Base
from configs.logging_config import logger
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from model.crud import get_user_by_username, create_user
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from utils.send_attendance_emails import send_daily_attendance_emails
from fastapi.middleware.cors import CORSMiddleware

import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to initialize the database and create root user if not exists.
    """
    print("Starting Application...")
    # Initialize the database session
    db_session.configure(bind=engine)
    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("DB tables created")
    # Measure time taken to create tables
    start_time = time.time()
    Base.metadata.create_all(bind=engine) # Create tables if they don't exist 
    create_all_time = time.time()
    print(f"DB schema creation took {create_all_time - start_time:.2f} seconds")
    root_username = "root"
    root_email = "rootadmin@example.com"
    root_password = "password" # Default password
    root_user_by_username = get_user_by_username(db_session, root_username)
    root_user_by_email = db_session.query(User).filter_by(email=root_email).first()
    
    # Check if root user exists by username or email
    if not root_user_by_username and not root_user_by_email:
        create_user(db_session, {
            "emp_id": "root001",
            "username": root_username,
            "email": root_email,
            "password": root_password,
            "department": "Administration",
            "sub_department": "Root",
        }, is_admin=True)
    # APScheduler setup for attendance emails
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_attendance_emails, 'cron', day_of_week='mon-fri', hour=7, minute=0)
    scheduler.start()
    print("Scheduler started. Waiting for next run...")
    yield

app = FastAPI(docs_url="/docs", lifespan=lifespan)

app.include_router(user_routes.router)


# Middleware for CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000, help="Port to run the app on")
args = parser.parse_args()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip preflight requests
        if request.method == "OPTIONS":
            return await call_next(request)
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}ms")
        return response

app.add_middleware(LoggingMiddleware)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(args.port))
