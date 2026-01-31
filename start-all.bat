@echo off
echo Starting Physical AI & Humanoid Robotics development servers...

REM Start backend server in a new window
start "Backend Server" cmd /k "cd /d D:\Hackathon-1\PhysicalAI_Book\server && node server.js"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server in a new window
start "Frontend Server" cmd /k "cd /d D:\Hackathon-1\PhysicalAI_Book\frontend && npx docusaurus start"

echo Both servers are starting...
echo Backend: http://localhost:3001
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul