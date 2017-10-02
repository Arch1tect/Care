from flask import Flask, send_file

import setup
from db_session import session
from db.model import CareTask, TaskLog
from snapshot import take_snapshot

app = Flask(__name__)


@app.route("/snapshot/<task_id>")
def get_snapshot(task_id):
	'''Get snapshot of existing task'''
	task = session.query(CareTask).filter(CareTask.id==task_id).one()
	new_snapshot_name = '{}-{}.png'.format(task.id, task.last_run_id + 1)
	new_snapshot_path = '../snapshot/{}'.format(new_snapshot_name)

	take_snapshot(task, new_snapshot_path, new_snapshot_name)

	return send_file(new_snapshot_path, mimetype='image/png')


@app.route("/task/name/<path:url>")
def create_new_task(url):
	'''Get snapshot of existing task'''
	pass

# @app.route("/snapshot/<name>/<path:url>")
# def get_snapshot(name, url):



# 	return 'hi'

app.run(port=8080)
