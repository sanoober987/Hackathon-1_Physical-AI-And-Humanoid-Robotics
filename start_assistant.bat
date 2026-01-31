@echo off
REM Script to run the AI-Powered Physical AI Assistant system on Windows

echo 🚀 Starting AI-Powered Physical AI Assistant System...

REM Check if we're in the right directory
if not exist "PhysicalAI_Book\server" (
    echo ❌ Error: PhysicalAI_Book\server directory not found!
    echo Please run this script from the root directory containing PhysicalAI_Book\
    pause
    exit /b 1
)

if not exist "PhysicalAI_Book\frontend" (
    echo ❌ Error: PhysicalAI_Book\frontend directory not found!
    echo Please run this script from the root directory containing PhysicalAI_Book\
    pause
    exit /b 1
)

echo 📦 Starting backend server...
cd PhysicalAI_Book\server

REM Install dependencies
echo 📦 Installing backend dependencies...
npm install

REM Start the backend server in a separate window
echo 🏃 Starting Express server on port 3001...
start cmd /k "cd /d %~dp0PhysicalAI_Book\server && npm start"

echo ✅ Backend server started successfully

REM Move to frontend directory
cd ..\frontend

REM Install dependencies
echo 📦 Installing frontend dependencies...
npm install

REM Start the frontend server in a separate window
echo 🏃 Starting Docusaurus server on port 3000...
start cmd /k "cd /d %~dp0PhysicalAI_Book\frontend && npm start"

echo ✅ Frontend server started successfully

echo.
echo 🎉 AI-Powered Physical AI Assistant System is now running!
echo.
echo 🌐 Access the system:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:3001
echo    Health check: http://localhost:3001/health
echo.
echo 🤖 Assistant endpoints:
echo    POST /assistant/chat - Chat with AI assistant
echo    GET /assistant/capabilities - Get assistant capabilities
echo    GET /health - Health check
echo.
echo 📌 Features available:
echo    • Natural language understanding for Physical AI concepts
echo    • Multi-language support (English and Urdu)
echo    • Context-aware responses using RAG
echo    • Knowledge of robotics, sensors, actuators, and humanoid systems
echo    • Real-time information retrieval
echo    • Intelligent question answering
echo.
echo Press any key to exit...
pause >nul