from flask import Flask, redirect, jsonify
import subprocess
import os
import time

app = Flask(__name__)

AVAILABLE_COMMANDS = ['sync_github', 'restart_app', 'clone_repo','start_app', 'stop_app',
                      'delete_repo', 'start_telegram_bot', 'stop_telegram_bot']

repo_uri = "git@github.com:mehmet-zahid/mengine.git"

print(os.path.abspath(os.path.dirname(__file__)))

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

@app.get('/restart_app')
def restart_project():...

@app.get('/clone_repo')
def clone_repo():...

@app.get('/delete_repo')
def delete_repo():...

@app.get('/start_telegram_bot')
def start_telegram_bot():...

@app.get('/stop_telegram_bot')
def stop_telegram_bot():...

@app.get('/start_app')
def start_app():...
    

def _start_app():
    commands = [{'celery': 'cd mengine/ && celery -A app.celery worker',
                'main_app': 'cd mengine/ && python3 app.py',
                'flower': 'cd mengine/ && celery -A app.celery flower --port=5002',
                'redis': 'redis-server'}]
    redirect('/sync_github')
    for command in commands:
        try:
            print(f'executing command: {command} ')
            subprocess.Popen(command, shell=True)
            time.sleep(2)
        except Exception as e:
            print(e)

def _restart_app():...

def _stop_app():...


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)


