from flask import Flask, redirect, jsonify
import subprocess
import time
import logging

app = Flask(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

AVAILABLE_COMMANDS = ['sync_aiengine', 'sync_manager', 'restart_app', 'clone_repo','start_app', 'stop_app',
                      'delete_repo', 'start_telegram_bot', 'stop_telegram_bot']

repo_uri = "git@github.com:mehmet-zahid/aiengine.git"

INITIAL_PARAMS = [{
    "name": "redis",
    "command": "redis-server",
    "priority": 1
    },
    {
    "name": "celery",
    "command": "cd /home/aiengine/recram_ai && celery --app=app.celery worker -l info",
    "priority": 2
    },
    {
    "name": "flower",
    "command": "cd /home/aiengine/recram_ai && celery -A app.celery flower --port=5002",
    "priority": 3
    },
    {
    "name": "main",
    "command": "cd /home/aiengine/recram_ai && gunicorn -w 3 app:app -b 0.0.0.0:5000",
    "priority": 4
    }]

commands = {
    'celery': f'cd /home/aiengine/recram_ai && celery -A app.celery worker -l info',
    'main_app': f'cd /home/aiengine/recram_ai && gunicorn -w 3 app:app -b 0.0.0.0:5000',
    'flower': f'cd /home/aiengine/recram_ai && celery -A app.celery flower --port=5002',
    'redis': 'redis-server --port 6379'
    }

ordered_cmd = {
        1:commands['redis'],
        2:commands['celery'],
        3:commands['flower'],
        4:commands['main_app']}

runningProcesses: dict[int,subprocess.Popen] = {}

@app.get('/')
def help():
    return AVAILABLE_COMMANDS


@app.get('/sync_aiengine')
def sync_github():
    logger.info('[*] Attemting to sync aiengine with remote github repo ...')
    return _sync_repo(repo_path='/home/aiengine')

    

@app.get('/sync_manager')
def sync_manager():
    logger.info('[*] Attemting to sync manager with remote github repo...')
    return _sync_repo(repo_path='/home/engine-manager')

@app.get('/clone_repo')
def clone_repo():...

@app.get('/delete_repo')
def delete_repo():...

@app.get('/start_telegram_bot')
def start_telegram_bot():...

@app.get('/stop_telegram_bot')
def stop_telegram_bot():...

@app.get('/start_app')
def start_app():
    res = _start_app()
    return res

@app.get('/restart_app')
def restart_app():
    _stop_app()
    time.sleep(5)
    _start_app()
    return jsonify({'success': True, 'message': 'Restarted app successfully'})


@app.get('/stop_app')
def stop_app():
    res= _stop_app()
    return res
    
def _sync_repo(repo_path: str):
    try:
        p =subprocess.Popen(f'cd {repo_path} && git pull',shell=True, stdout=subprocess.PIPE, text=True)
    except Exception as e:
        logger.info(f'[*] Exception: {e}')
        return jsonify({'error': True, 'message': str(e)}) 

    logger.info('[*] Waiting for the result ...')
    for i in range(2):
        try:
            r = p.communicate(timeout=10)[0]
            logger.info('Succesfully synchronized repository')
            return jsonify({'success': True,
                        'message': 'Succesfully synchronized repository',
                        'result': r})
        except TimeoutError :
            logger.info('[*] TimeoutError. Retrying ...')
        

    logger.info('Failed to sync repository. Try again later.')
    return jsonify({'error': True, 'message': 'Failed to sync repository'})

def _start_app():
    global runningProcesses
    if len(runningProcesses)==0:
        for element in INITIAL_PARAMS:
            try:
                logger.info(f'Starting {element["name"]}')
                logger.info(f'[*] Executing {element["priority"]}: {element["command"]}')
                p=subprocess.Popen(element["command"], shell=True)
                runningProcesses[element["priority"]] = p
                time.sleep(2)
            except Exception as e:
                logger.error(f'Failed to execute {element["priority"]}: {element["command"]}')
                logger.error(e)
        return jsonify({'success': True, 'message': 'service has been successfully initialized .'})
    else:
        return jsonify({'success': False, 'message': 'service has minumum one process running! \
            \nFirst stop all running processes!'})


def _stop_app():
    global runningProcesses
    run_proc = runningProcesses.copy()
    lentgh_run_proc = len([k for k, v in runningProcesses.elements()])
    if lentgh_run_proc != 0:
        results = {}
        logger.info(f"results: {results}")
        for num,proc in run_proc.items():
            try:
                logger.info(f'[*] Stopping process {num}: {proc}')
                runningProcesses[num].kill()
                runningProcesses.pop(num)
                results[f"{num}--> {proc}"] = 'success'
                logger.info(f"results: {results}")
                time.sleep(2)
            except Exception as e:
                logger.error(f'Failed to stop process {num}: {proc}')
                logger.info(f"results: {results}")
                results[f"{num}--> {proc}"] = 'failure'
        
        return jsonify(results)
    logger.info('[*] No running processes')
    return jsonify({'success': False, 'message':'No running processes'})


if __name__ == "__main__":
    #with app.app_context():
    _start_app()
    app.run(host="0.0.0.0", port=5001)


