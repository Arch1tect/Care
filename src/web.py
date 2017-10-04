import time

from flask import Flask, send_file, make_response

import setup
from db_session import session
from db.model import CareTask, TaskLog
from snapshot import take_snapshot

app = Flask(__name__)


@app.route("/task/<task_id>/snapshot")
def get_snapshot_for_task(task_id):
	'''Get snapshot of existing task'''
	task = session.query(CareTask).filter(CareTask.id==task_id).one()
	new_snapshot_name = '{}-{}.png'.format(task.id, task.last_run_id + 1)
	new_snapshot_path = '../snapshot/{}'.format(new_snapshot_name)

	if take_snapshot(task, new_snapshot_path):
		return send_file(new_snapshot_path, mimetype='image/png')
	return 'Failed to take snapshot.'


@app.route("/snapshot/<path:url>")
def take_snapshot_for_url(url):
	url = url.lower()
	if not url.startswith('http'):
		url = 'http://' + url
	task = CareTask(id=0, name='new', url=url)
	snapshot_path = '../snapshot/{}.png'.format(time.time())
	if take_snapshot(task, snapshot_path):
		response = make_response(send_file(snapshot_path, mimetype='image/png'))
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response
	return 'Failed to take snapshot.'

# TODO debug=True only for dev environment
app.run(debug=True, port=8080)
