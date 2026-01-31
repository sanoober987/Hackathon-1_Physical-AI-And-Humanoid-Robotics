"""
Script to start the Physical AI Assistant backend
"""
import subprocess
import sys
import os
import signal
import time
from threading import Thread

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "PhysicalAI_Book/backend/requirements.txt"])
    print("Dependencies installed successfully!")

def start_backend():
    """Start the FastAPI backend"""
    print("Starting Physical AI Assistant backend...")

    # Change to backend directory
    os.chdir("PhysicalAI_Book/backend")

    # Run the uvicorn server
    cmd = [sys.executable, "-c",
           "import uvicorn; from app import app; uvicorn.run(app, host='0.0.0.0', port=8000)"]

    process = subprocess.Popen(cmd)

    try:
        print("Backend started on http://localhost:8000")
        print("Press Ctrl+C to stop the server")
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down backend...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("Backend stopped.")

if __name__ == "__main__":
    # Install dependencies first
    install_dependencies()

    # Start the backend
    start_backend()