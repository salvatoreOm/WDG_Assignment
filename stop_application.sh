#!/bin/bash

echo "🛑 Stopping NGO Impact Tracker Application"
echo "==========================================="

# Check if PIDs file exists
if [ -f .pids ]; then
    # Read PIDs from file
    PIDS=$(cat .pids)
    echo "📋 Found running services with PIDs: $PIDS"
    
    # Kill each process
    for PID in $PIDS; do
        if kill -0 $PID 2>/dev/null; then
            echo "🔴 Stopping process $PID..."
            kill $PID
        else
            echo "⚠️  Process $PID not running"
        fi
    done
    
    # Clean up PIDs file
    rm -f .pids
else
    echo "⚠️  No .pids file found. Trying to stop common processes..."
    
    # Try to stop common processes
    pkill -f "python manage.py runserver"
    pkill -f "celery.*worker"
    pkill -f "npm start"
fi

# Clean up log files
rm -f django.log celery.log

echo "✅ All services stopped successfully!"
echo "💡 To start again, run: ./start_application.sh" 