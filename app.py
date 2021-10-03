from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import nipyapi
from random import randrange
import time



app = Flask(__name__)
nipyapi.config.nifi_config.host = 'http://localhost:8080/nifi-api'
nipyapi.config.registry_config.host = 'http://localhost:18080/nifi-registry-api'
root_id = nipyapi.canvas.get_root_pg_id()
root_process_group = nipyapi.canvas.get_process_group(root_id, 'id')
nipyapi.canvas.schedule_process_group(root_id, False)
starttime=time.time()


@app.route('/')
def index():
    nipyapi.canvas.schedule_process_group(root_id, False)
    return render_template('main.html')


@app.route('/about')
def about():
    return 'About page'


@app.route('/nifi', methods=['POST', 'GET'])
def nifi():
    if request.method == 'POST':
        nipyapi.canvas.update_variable_registry(root_process_group, ([('test1', '2')]))
        nipyapi.canvas.schedule_process_group(root_id, True)
        time.sleep(2 - ((time.time() - starttime) % 2))
        while nipyapi.canvas.get_process_group_status('017c100b-ee54-138e-cb41-7a1d45803b1c', 'names') == '':
            time.sleep(2 - ((time.time() - starttime) % 2))
        else:
            nipyapi.canvas.schedule_process_group(root_id, False)
        return nipyapi.canvas.get_process_group_status('017c100b-ee54-138e-cb41-7a1d45803b1c', 'names')
    else:
        return render_template('go_to_nifi.html')


if __name__ == "__main__":
    app.run(debug=True)