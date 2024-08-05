echo "Starting Redis server..."
start cmd /k "redis-server"

echo "Starting backend application..."
start cmd /k "cd backend && python app.py"

echo "Starting Celery beat..."
start cmd /k "cd backend && celery -A app.celery beat --loglevel=info"

echo "Starting Celery worker..."
start cmd /k "cd backend && celery -A app.celery worker --pool=solo --loglevel=info"

echo "Starting frontend application..."
start cmd /k "cd frontend && npm run serve"

echo "All services started successfully!"