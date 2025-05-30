from sqlalchemy import Column, Integer, String,Boolean, Date, Time, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import date, datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    emp_id = Column(String, unique=True, nullable=False)  # Added emp_id
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    department = Column(String, nullable=True)
    sub_department = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    attendances = relationship("Attendance", back_populates="user")
    access_logs = relationship("AccessLog", back_populates="user")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(Date, default=date.today)
    status = Column(String)
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    user = relationship("User", back_populates="attendances")

class AccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    emp_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String, nullable=False)  # 'IN' or 'OUT'
    user = relationship("User", back_populates="access_logs")
    
class ResetToken(Base):
    __tablename__ = "reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
