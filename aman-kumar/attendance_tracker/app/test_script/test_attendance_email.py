import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# add parent directory to path
from utils.send_attendance_emails import send_daily_attendance_emails

if __name__ == "__main__":
    send_daily_attendance_emails()
    print("Attendance email job executed for testing.")
