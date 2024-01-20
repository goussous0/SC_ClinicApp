@echo off
set APP_MODULE=main:app

echo Running Uvicorn...
uvicorn %APP_MODULE% --host 0.0.0.0 --port 80  --reload

pause
