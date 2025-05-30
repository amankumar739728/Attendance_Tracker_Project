from sqlalchemy.orm import Session
from model.models import User, Attendance
from fastapi import HTTPException, status
from passlib.hash import bcrypt
from datetime import date

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data: dict, is_admin: bool = False):
    if get_user_by_username(db, user_data["username"]):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        emp_id=user_data["emp_id"],  # Store emp_id
        username=user_data["username"],
        email=user_data["email"],
        password_hash=bcrypt.hash(user_data["password"]),
        department=user_data["department"],
        sub_department=user_data["sub_department"],
        is_admin=is_admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, current_user: User, username: str, updated_data: dict):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to update users")

    # Prevent removing admin rights from root admin user
    if user.username == "root" and "is_admin" in updated_data and not updated_data["is_admin"]:
        raise HTTPException(status_code=403, detail="Cannot remove admin rights from root admin user")

    for key, value in updated_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, current_user: User, username: str):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to delete users")
    # Prevent deletion of root admin user
    if user.username == "root":
        raise HTTPException(status_code=403, detail="Root admin user cannot be deleted")
    db.delete(user)
    db.commit()
    return {"detail": f"User '{username}' deleted successfully"}

def mark_attendance(db: Session, user: User, check_in_time, check_out_time):
    today = date.today()
    existing = db.query(Attendance).filter_by(user_id=user.id, date=today).first()
    if existing:
        existing.check_out = check_out_time
    else:
        record = Attendance(
            user_id=user.id,
            date=today,
            status="Present",
            check_in=check_in_time,
            check_out=check_out_time
        )
        db.add(record)
    db.commit()
    return {"message": "Attendance recorded"}

def get_attendance_by_user(db: Session, user_id: int):
    return db.query(Attendance).filter_by(user_id=user_id).all()

def get_attendance_today(db: Session, user_id: int):
    return db.query(Attendance).filter_by(user_id=user_id, date=date.today()).first()