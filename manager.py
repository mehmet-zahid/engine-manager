from flask import Flask, redirect, jsonify
import subprocess
import time


app = Flask(__name__)

AVAILABLE_COMMANDS = ['sync_github', 'restart_app', 'clone_repo','start_app', 'stop_app',
                      'delete_repo', 'start_telegram_bot', 'stop_telegram_bot']

repo_uri = "git@github.com:mehmet-zahid/mengine.git"
VENV_CMD = "source /home/venv/bin/activate"

commands = {
    'celery': f'{VENV_CMD}&&cd /home/mengine/recram_ai && celery -A app.celery worker',
    'main_app': f'{VENV_CMD}&&cd /home/mengine/recram_ai && gunicorn -w 3 app:app -b 0.0.0.0:5000',
    'flower': f'{VENV_CMD}&&cd /home/mengine/recram_ai && celery -A app.celery flower --port=5002',
    'redis': 'redis-server --port 7979'
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


@app.get('/sync_github')
def sync_github():
    print('[*] Attemting to sync ...')
    print('[*] Syncing with github')
    p =subprocess.Popen(f'cd mengine/ && git pull origin',
                        shell=True, stdout=subprocess.PIPE, text=True)
    for i in range(2):
        try:
            print('[*] Waiting for the result ...')
            r = p.communicate(timeout=5)[0]
            print('Succesfully synchronized repository')
            return jsonify({'success': True,
                        'message': 'Succesfully synchronized repository',
                        'result': r})
        except TimeoutError :
            print('[*] TimeoutError. Retrying ...')

    print('Failed to sync repository. Try again later.')
    return jsonify({'success': False,'message': 'Failed to sync repository'})


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
    _stop_app
    time.sleep(5)
    _start_app
    return jsonify({'success': True, 'message': 'Restarted app successfully'})


@app.get('/stop_app')
def stop_app():
    res= _stop_app()
    return res
    

def _start_app():
    global runningProcesses
    if len(runningProcesses)==0:
        for i in range(len(ordered_cmd)):
            try:
                print(f'[*] executing command: {ordered_cmd[i+1]} ')
                p=subprocess.Popen(ordered_cmd[i+1], shell=True, executable='/bin/bash')
                runningProcesses[i+1] = p
                time.sleep(2)
            except Exception as e:
                print('Failed to execute command')
                print(e)
        return jsonify({'success': True, 'message': 'app has been run successfully.'})
    else:
        return jsonify({'success': False, 'message': 'app is already running !'})


def _stop_app():
    if len(runningProcesses) != 0:
        results = {}
        for proc in runningProcesses:
            try:
                print(f'[*] Stopping process: {proc}')
                runningProcesses[proc].kill()
                results[f'command {proc}'] = 'success'
                time.sleep(2)
            except Exception as e:
                print(f'Failed to stop process: {proc}')
                results[f'command {proc}'] = 'failure'
        return jsonify(results)
    print('[*] No running processes')
    return jsonify({'success': False, 'message':'No running processes'})


if __name__ == "__main__":
    with app.app_context():
        _start_app()
    app.run(host="0.0.0.0",port=5001)


