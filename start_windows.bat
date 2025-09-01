@echo off
echo Starting CLO/PLO Assessment Platform...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Install backend dependencies
echo Installing backend dependencies...
cd backend\clo_assessment_api
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)

REM Start backend
echo Starting backend server...
start "Backend Server" python src\enhanced_api.py

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend (serve static files)
echo Starting frontend server...
cd ..\..\frontend
python -m http.server 3000

pause
