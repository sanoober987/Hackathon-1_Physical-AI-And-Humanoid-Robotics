#!/bin/bash
# Script to run the Physical AI & Humanoid Robotics RAG system

echo "🚀 Starting Physical AI & Humanoid Robotics RAG System..."

# Check if we're in the right directory
if [ ! -d "PhysicalAI_Book/backend" ] || [ ! -d "PhysicalAI_Book/frontend" ]; then
    echo "❌ Error: PhysicalAI_Book directory structure not found!"
    echo "Please run this script from the root directory containing PhysicalAI_Book/"
    exit 1
fi

# Function to start backend
start_backend() {
    echo "📦 Starting backend server..."
    cd PhysicalAI_Book/backend

    # Check if virtual environment exists, if not create it
    if [ ! -d ".venv" ]; then
        echo "🔧 Creating virtual environment..."
        python -m venv .venv
    fi

    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi

    # Install dependencies
    echo "📦 Installing backend dependencies..."
    pip install -r requirements.txt

    # Start the backend server
    echo "🏃 Starting FastAPI server on port 8000..."
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!

    # Wait a moment for the server to start
    sleep 3

    # Check if backend started successfully
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "✅ Backend server started successfully (PID: $BACKEND_PID)"
    else
        echo "❌ Failed to start backend server"
        exit 1
    fi

    cd ../..
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting frontend server..."
    cd PhysicalAI_Book/frontend

    # Install dependencies
    echo "📦 Installing frontend dependencies..."
    npm install

    # Start the frontend server
    echo "🏃 Starting Docusaurus server on port 3000..."
    npm start &
    FRONTEND_PID=$!

    # Wait a moment for the server to start
    sleep 5

    # Check if frontend started successfully
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "✅ Frontend server started successfully (PID: $FRONTEND_PID)"
    else
        echo "❌ Failed to start frontend server"
        exit 1
    fi

    cd ../..
}

# Start both servers
start_backend
start_frontend

echo ""
echo "🎉 Physical AI & Humanoid Robotics RAG System is now running!"
echo ""
echo "🌐 Access the system:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "💬 Chatbot endpoints:"
echo "   POST /api/v1/chat/ - Normal QA"
echo "   POST /api/v1/chat/selected - Selected text QA"
echo ""
echo "📌 Features available:"
echo "   • Normal QA from the whole book"
echo "   • Selected-text QA with highlighted text"
echo "   • Personalized answers based on user profile"
echo "   • Urdu translation support"
echo "   • Rate limiting"
echo "   • Conversation logging"
echo "   • Source citations"
echo ""
echo "📝 Press Ctrl+C to stop the system"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID