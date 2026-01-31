#!/bin/bash
# Script to run the AI-Powered Physical AI Assistant system

echo "🚀 Starting AI-Powered Physical AI Assistant System..."

# Check if we're in the right directory
if [ ! -d "PhysicalAI_Book/server" ] || [ ! -d "PhysicalAI_Book/frontend" ]; then
    echo "❌ Error: PhysicalAI_Book directory structure not found!"
    echo "Please run this script from the root directory containing PhysicalAI_Book/"
    exit 1
fi

# Function to start backend
start_backend() {
    echo "📦 Starting Express backend server..."
    cd PhysicalAI_Book/server

    # Install dependencies
    echo "📦 Installing backend dependencies..."
    npm install

    # Start the backend server
    echo "🏃 Starting Express server on port 3001..."
    npm start &
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
echo "🎉 AI-Powered Physical AI Assistant System is now running!"
echo ""
echo "🌐 Access the system:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:3001"
echo "   Health check: http://localhost:3001/health"
echo ""
echo "🤖 Assistant endpoints:"
echo "   POST /assistant/chat - Chat with AI assistant"
echo "   GET /assistant/capabilities - Get assistant capabilities"
echo "   GET /health - Health check"
echo ""
echo "📌 Features available:"
echo "   • Natural language understanding for Physical AI concepts"
echo "   • Multi-language support (English and Urdu)"
echo "   • Context-aware responses using RAG"
echo "   • Knowledge of robotics, sensors, actuators, and humanoid systems"
echo "   • Real-time information retrieval"
echo "   • Intelligent question answering"
echo ""
echo "📝 Press Ctrl+C to stop the system"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID