@echo off
echo Starting Physical AI & Humanoid Robotics development servers...

echo.
echo ================================================
echo Starting Backend Server (Port 3001)...
echo ================================================
echo.

REM Start backend server in a new window
start "Backend Server - Physical AI" cmd /k "cd /d D:\Hackathon-1\PhysicalAI_Book\server && echo Starting backend server... && node server.js && pause"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo Starting Frontend Server (Port 3000)...
echo ================================================
echo.

REM Start frontend server in a new window
start "Frontend Server - Physical AI" cmd /k "cd /d D:\Hackathon-1\PhysicalAI_Book\frontend && echo Starting frontend server... && npx docusaurus start && pause"

echo.
echo ================================================
echo Servers Starting...
echo ================================================
echo Backend: http://localhost:3001
echo Frontend: http://localhost:3000
echo AI Assistant: http://localhost:3000/assistant
echo.
echo NOTE: The backend server runs on port 3001
echo       The frontend runs on port 3000
echo       The AI Assistant will be available at /assistant
echo.
echo Press any key to exit...
pause >nul