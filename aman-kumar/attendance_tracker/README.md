## step1: cd C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025\workarea\aman-kumar\attendance_tracker

## step2: py311\Scripts\activate

## Run the Application using below command:
   ## step-3: python app/main.py --port=9123

   ## step-4: once the server will be started then for swagger page type the below link and access the page for api check:
 # Link: http://127.0.0.1:9123/docs

## uvicorn app.main:app --reload     #if app port is not configured



## for testing of sending mail follow the below steps or run the test script(test_attendance_email.py):

## (py311) C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025\workarea\aman-kumar\attendance_tracker>python app\test_script\test_attendance_email.py


## make the below change in send_attendance_emails.py as below:

  # scheduler.add_job(send_daily_attendance_emails, 'interval', minutes=1) # change this to 1 minute for testing


# For email sending keep the generated password in .env file:
  
  # step1: go to the link : https://myaccount.google.com/security
  # step-2: in the search bar type App passwords and give a name to App and copy the password and save it to .env file
  # step-3: username will be email