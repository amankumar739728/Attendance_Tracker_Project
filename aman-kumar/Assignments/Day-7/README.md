## Project Overview:

## This Project is all about creating a CRUD operation on user created inside sqlite3(no need to install using pip command) and generating a bearer token(access_token) for Endpoint validation.

## command to run the FastAPI Application:

# go to Day-7(project) folder using:=>  cd <relative-project-folder> e.g: cd workarea\aman-kumar\Assignments\Day-7

# --> general steps to fastapi Application if ports are not configured:
   # uvicorn main:app --port 8000 --reload

## If port is configured as an argument to be passed:
   # (venv) C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025\workarea\aman-kumar\Assignments\Day-7>python main.py --port=9123


## Swagger DOCS ACCESS:

# For Accessing Swagger follow the below link after starting the APP on localhost(127.0.0.1) using above python command :

   # http://127.0.0.1:8000/docs   ==> by default port:8000 if you are not passing it in python command
   # http://127.0.0.1:9123/docs   ==> access the swagger docs by typing this url in chrome browser