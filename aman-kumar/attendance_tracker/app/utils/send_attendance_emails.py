from datetime import datetime, timedelta, date
import calendar
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session
from model.models import User, AccessLog
from configs.database import db_session
from utils.email_utils import send_email, generate_email_body
from configs.config import settings

def send_daily_attendance_emails():
    yesterday = date.today() - timedelta(days=1)
    # Skip if yesterday is Saturday (5) or Sunday (6)
    if yesterday.weekday() in [5, 6]:
        print("No attendance emails sent for weekends.")
        return
    day_str = yesterday.strftime("%A")
    date_str = yesterday.strftime("%d-%b-%Y")
    users = db_session.query(User).all()
    for user in users:
        # Skip root user
        if user.email == "rootadmin@example.com":
            continue
        logs = db_session.query(AccessLog).filter(
            AccessLog.user_id == user.id,
            AccessLog.timestamp.between(
                datetime.combine(yesterday, datetime.min.time()),
                datetime.combine(yesterday, datetime.max.time())
            )
        ).order_by(AccessLog.timestamp).all()
        in_time = next((l.timestamp for l in logs if l.action == "IN"), None)
        out_time = next((l.timestamp for l in reversed(logs) if l.action == "OUT"), None)
        # If no attendance, mark as ABSENT
        if not in_time and not out_time:
            in_time = out_time = "ABSENT"
        email_body = generate_email_body(
            name=user.username,
            dept=user.department or "",
            sub_dept=user.sub_department or "",
            in_time=in_time,
            out_time=out_time,
            date_str=date_str,
            day_str=day_str
        )
        send_email(
            to_email=user.email,
            subject=f"Your Attendance Details for {date_str}",
            html_content=email_body
        )
        print(f"Sent attendance email to {user.email}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Schedule to run every weekday at 7:00 AM
    scheduler.add_job(send_daily_attendance_emails, 'cron', day_of_week='mon-fri', hour=7, minute=0)
    ## uncomment the below line to test the email sending functionality(run every minute)
    #scheduler.add_job(send_daily_attendance_emails, 'interval', minutes=1)
    print("Scheduler started. Waiting for next run...")
    scheduler.start()
