#!/bin/bash
echo "Starting CLO/PLO Assessment Platform..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed"
    exit 1
fi

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend/clo_assessment_api
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install backend dependencies"
    exit 1
fi

# Start backend
echo "Starting backend server..."
python3 src/enhanced_api.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend server..."
cd ../../frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo "Platform started successfully!"
echo "Backend: http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
