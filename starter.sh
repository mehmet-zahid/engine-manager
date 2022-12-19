#!/bin/bash

source /home/venv/bin/activate
redis-server --port 7979 &
echo "redis-server started "
sleep 2
(cd /home/mengine/recram_ai && celery -A app.celery worker)&
echo "celery worker started "
sleep 3
celery -A app.celery flower --port=5002 &
echo "celery flower started "
sleep 3
gunicorn -w 3 app:app -b 0.0.0.0:5000 &
echo "gunicorn started "
