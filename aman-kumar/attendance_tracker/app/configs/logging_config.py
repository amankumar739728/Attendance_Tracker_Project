import logging
import sys
import os
from datetime import datetime, timedelta

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Generate log filename with current date
log_date = datetime.now().strftime('%Y-%m-%d')
log_filename = f'logs/attendance_tracker_{log_date}.log'

# Delete log files older than 3 days
now = datetime.now()
for fname in os.listdir('logs'):
    if fname.startswith('attendance_tracker_') and fname.endswith('.log'):
        try:
            date_str = fname[len('attendance_tracker_'):-len('.log')]
            file_date = datetime.strptime(date_str, '%Y-%m-%d')
            if (now - file_date).days > 3:
                os.remove(os.path.join('logs', fname))
        except Exception:
            pass  # Ignore invalid file names

# Configure logging for the project
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('attendance_tracker')
