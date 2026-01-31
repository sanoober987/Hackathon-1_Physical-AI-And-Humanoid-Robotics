#!/bin/bash
# Script to start both frontend and backend servers for development

echo "Starting Physical AI & Humanoid Robotics development servers..."

# Start backend server in the background
echo "Starting backend server on port 3001..."
cd server
node server.js &
BACKEND_PID=$!

# Give backend a moment to start
sleep 2

# Start frontend server in the background
echo "Starting frontend server on port 3000..."
cd ../frontend
npx docusaurus start &
FRONTEND_PID=$!

# Function to stop servers on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap signals to cleanup on exit
trap cleanup SIGINT SIGTERM EXIT

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID