#!/bin/bash

echo "🚀 Starting NGO Impact Tracker Application"
echo "============================================"

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Please start Redis first:"
    echo "   redis-server"
    exit 1
fi

echo "✅ Redis is running"

# Start Django server in background
echo "🔧 Starting Django server..."
source venv/bin/activate
python manage.py runserver > django.log 2>&1 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Start Celery worker in background
echo "🔧 Starting Celery worker..."
celery -A ngo_impact_tracker worker --loglevel=info > celery.log 2>&1 &
CELERY_PID=$!

# Wait a moment for Celery to start
sleep 3

# Start React frontend
echo "🔧 Starting React frontend..."
cd frontend
npm start &
REACT_PID=$!

echo ""
echo "🎉 All services started!"
echo "========================"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API:      http://localhost:8000/api"
echo ""
echo "📊 Logs:"
echo "Django: tail -f django.log"
echo "Celery: tail -f celery.log"
echo ""
echo "🛑 To stop all services:"
echo "kill $DJANGO_PID $CELERY_PID $REACT_PID"

# Store PIDs for cleanup
echo "$DJANGO_PID $CELERY_PID $REACT_PID" > .pids

echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap 'echo ""; echo "🛑 Stopping all services..."; kill $DJANGO_PID $CELERY_PID $REACT_PID 2>/dev/null; rm -f .pids django.log celery.log; echo "✅ All services stopped"; exit 0' INT

# Keep script running
wait 