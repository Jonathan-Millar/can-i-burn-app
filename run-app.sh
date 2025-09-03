#!/bin/bash

echo "🚀 Starting Canada Fire Watch Application..."
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start Flask backend
echo "🔧 Starting Flask backend on port 5000..."
cd src
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/api/enhanced/provinces > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:5000"
else
    echo "❌ Backend failed to start. Check the logs above."
    exit 1
fi

echo ""

# Start React frontend
echo "🌐 Starting React frontend on port 3000..."
npm run dev &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running on http://localhost:3000"
else
    echo "❌ Frontend failed to start. Check the logs above."
    exit 1
fi

echo ""
echo "🎉 Application is running!"
echo ""
echo "🔗 Backend API: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for user to stop
wait
