from email.message import EmailMessage
import smtplib
from configs.config import settings
from datetime import datetime

def generate_email_body(name, dept, sub_dept, in_time, out_time, date_str=None, day_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%d-%b-%Y")
    if not day_str:
        day_str = datetime.now().strftime("%A")
    # Handle 'ABSENT' case and format times
    if isinstance(in_time, str):
        if in_time == "ABSENT":
            in_time_fmt = "ABSENT"
        else:
            in_time = datetime.strptime(in_time, "%Y-%m-%d %H:%M:%S")
            in_time_fmt = in_time.strftime("%d-%b-%Y %H:%M:%S")
    else:
        in_time_fmt = in_time.strftime("%d-%b-%Y %H:%M:%S") if in_time else "N/A"
    if isinstance(out_time, str):
        if out_time == "ABSENT":
            out_time_fmt = "ABSENT"
        else:
            out_time = datetime.strptime(out_time, "%Y-%m-%d %H:%M:%S")
            out_time_fmt = out_time.strftime("%d-%b-%Y %H:%M:%S")
    else:
        out_time_fmt = out_time.strftime("%d-%b-%Y %H:%M:%S") if out_time else "N/A"

    return f"""
    <html><body>
    <p>Hello {name},</p>
    <p>Below is your attendance details at GyanSys Office:</p>
    <table border="1" cellpadding="5">
        <tr><th>Date</th><th>Day</th><th>Employee Name</th><th>Department</th><th>Sub-Department</th><th>In Time</th><th>Out Time</th></tr>
        <tr><td>{date_str}</td><td>{day_str}</td><td>{name}</td><td>{dept}</td><td>{sub_dept}</td><td>{in_time_fmt}</td><td>{out_time_fmt}</td></tr>
    </table>
    <br><p>Thank You,</p>
    <p><i>Note: This is an auto-generated email from Attendance Tool. The same is being shared with your Manager. Please ignore this email, if you are working from Client Location.</i></p>
    </body></html>
    """

def send_email(to_email, subject, html_content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content("Please view in HTML")
    msg.add_alternative(html_content, subtype="html")

    # Use SMTP_SERVER from config, which is set from EMAIL_HOST in .env
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
        server.send_message(msg)

