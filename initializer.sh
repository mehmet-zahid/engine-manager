#!/bin/bash


stop_all_services(){
    echo "Stopping all services"
    docker ps -a --format "{{.Names}}" | docker container stop
    echo "All services stopped"
}

start_services(){
    echo "Starting services"
    docker ps -a --format "{{.Names}}" | docker container start
    echo "Started services"
}

restart_services(){
    echo "Restarting services"
    docker ps -a --format "{{.Names}}" | docker restart
    echo "Restart complete"
}

check_docker_installed(){
    if which docker > /dev/null; then
        echo "Docker is installed."
        docker --version
    else
        echo "Docker is not installed."
        echo "Installing latest stable docker ..."    
fi
}

check_docker_installed

: '

(redis-server --port 7979) &
echo "redis-server started "
sleep 2
cd /home/aiengine/recram_ai 
(celery -A app.celery worker) &
echo "celery worker started "
sleep 3
(celery -A app.celery flower --port=5002) &
echo "celery flower started "
sleep 3
(gunicorn -w 3 app:app -b 0.0.0.0:5000) &
echo "gunicorn started "
echo "AIENGINE is up ..."
'
