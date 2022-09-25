'''
Allows interaction with external devices
'''

import os
import socket
import time
import threading
from flask import Flask, jsonify
import requests
from smart_bed.status import get


IP = socket.gethostbyname(socket.gethostname() + '.local')
API_PORT = os.getenv('API_PORT')


def _run_api():
    try:
        app = Flask(__name__)

        @app.route('/status', methods=['GET'])
        def _get_status():
            return jsonify(get())

        app.run(host=IP, port=API_PORT)

    except Exception as error:
        print('ERROR: Running api', error)
        _run_api()


threading.Thread(target=_run_api).start()


def post_status():
    home_automation_url = os.getenv('HOME_AUTOMATION_URL')
    try:
        requests.post(home_automation_url, json=get(), timeout=5)

    except OSError:
        # if request fails, try again
        time.sleep(30)
        post_status()
