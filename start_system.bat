@echo off
REM Script to run the Physical AI & Humanoid Robotics RAG system on Windows

echo 🚀 Starting Physical AI & Humanoid Robotics RAG System...

REM Check if we're in the right directory
if not exist "PhysicalAI_Book\backend" (
    echo ❌ Error: PhysicalAI_Book\backend directory not found!
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
cd PhysicalAI_Book\backend

REM Check if virtual environment exists, if not create it
if not exist ".venv" (
    echo 🔧 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing backend dependencies...
pip install -r requirements.txt

REM Start the backend server in a separate window
echo 🏃 Starting FastAPI server on port 8000...
start cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo ✅ Backend server started successfully

REM Move to frontend directory
cd ..\frontend

REM Install dependencies
echo 📦 Installing frontend dependencies...
npm install

REM Start the frontend server in a separate window
echo 🏃 Starting Docusaurus server on port 3000...
start cmd /k "npm start"

echo ✅ Frontend server started successfully

echo.
echo 🎉 Physical AI & Humanoid Robotics RAG System is now running!
echo.
echo 🌐 Access the system:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 💬 Chatbot endpoints:
echo    POST /api/v1/chat/ - Normal QA
echo    POST /api/v1/chat/selected - Selected text QA
echo.
echo 📌 Features available:
echo    • Normal QA from the whole book
echo    • Selected-text QA with highlighted text
echo    • Personalized answers based on user profile
echo    • Urdu translation support
echo    • Rate limiting
echo    • Conversation logging
echo    • Source citations
echo.
echo Press any key to exit...
pause >nul