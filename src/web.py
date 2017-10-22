import time
import logging
import os

from flask import Flask, send_file, make_response, request

import setup
from db_session import session
from db.model import CareTask, TaskLog
from snapshot import take_snapshot

app = Flask(__name__)

logger = logging.getLogger(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    session.remove()

@app.route("/api/task/<task_id>/snapshot")
def get_snapshot_for_task(task_id):
	'''Get snapshot of existing task'''
	task = session.query(CareTask).filter(CareTask.id==task_id).one()
	new_snapshot_name = '{}-{}.png'.format(task.id, task.last_run_id + 1)
	new_snapshot_path = '../snapshot/{}'.format(new_snapshot_name)

	if take_snapshot(task, new_snapshot_path):
		return send_file(new_snapshot_path, mimetype='image/png')
	return 'Failed to take snapshot.'

@app.route("/api/task", methods=['POST'])
def create_new_task():
	'''Create new task'''

	# TODO: avoid duplicate
	data = request.get_json()
	url = correct_url(data['url'])
	logger.info('Creating new task with data {}'.format(data))
	task = CareTask(name=data.get('name'), url=url, interval=data['interval'], roi=data.get('roi'))
	session.add(task)
	session.commit()
		
	rand_snapshot = data.get('snapshot')
	if rand_snapshot:
		os.rename('../snapshot/{}'.format(rand_snapshot),
				  '../snapshot/{}-0.png'.format(task.id))

	return 'success'

@app.route("/api/screenshot/url", methods=['POST'])
def take_snapshot_for_url():
	data = request.get_json()
	url = correct_url(data['url'])
	task = CareTask(id=0, name='new', url=url)
	snapshot_name = '{}.png'.format(time.time())
	snapshot_path = '../snapshot/{}'.format(snapshot_name)
	if take_snapshot(task, snapshot_path):
		# response = make_response(send_file(snapshot_path, mimetype='image/png'))
		# response.headers['Access-Control-Allow-Origin'] = '*'
		return snapshot_name

	return 'Failed to take snapshot.', 500

def correct_url(url):
	if not url.startswith('http'):
		url = 'http://' + url
	return url

# TODO debug=True only for dev environment
app.run(debug=True, host='0.0.0.0', port=8088)
