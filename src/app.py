# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.model import CareTask
from cfg.credentials import db_user, db_password

from snapshot import take_snapshot, close_driver
from image_diff import compare_img
from mailgun import notify_change

# Always change directory to /src
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level = logging.INFO,
	filename = '/var/log/care.log'
	)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.INFO)

logging.getLogger('').addHandler(console_logger)

logger = logging.getLogger(__name__)



db_url = 'chat-anywhere-mysql.cjwz9xnh80ai.us-west-1.rds.amazonaws.com'
connection_str = 'mysql://{}:{}@{}'.format(db_user, db_password, db_url)
engine = create_engine(connection_str, encoding='utf8')
engine.execute("USE care")
DBSession = sessionmaker(bind=engine)
session = DBSession()

for t in session.query(CareTask).all():
	now = datetime.utcnow()
	new_snapshot_taken = False
	try:
		time_past = (now-t.last_run_time).total_seconds()
		# now_timestamp = int((now-datetime.utcfromtimestamp(0)).total_seconds())
		# last_run_time_timestamp = int((t.last_run_time-datetime.utcfromtimestamp(0)).total_seconds())
		if time_past >= t.interval:
			logger.info('[Task {}] last_run_time {}'.format(t.id, t.last_run_time))

			# get new snapshot
			old_snapshot_path = '../snapshot/{}-{}.png'.format(t.id, t.last_run_id)
			new_snapshot_name = '{}-{}.png'.format(t.id, t.last_run_id + 1)
			new_snapshot_path = '../snapshot/{}'.format(new_snapshot_name)
			
			# print old_snapshot_name
			new_snapshot_taken = take_snapshot(t, new_snapshot_path, new_snapshot_name)
			if new_snapshot_taken:

				t.last_run_id = t.last_run_id + 1
				t.last_run_time = now
				# ensure there's a previous snapshot to compare
				if os.path.isfile(old_snapshot_path):
					# compare new snapshot with old snapshot
					diff_img_name = '{}-{}.png'.format(t.id, t.last_run_id+1)
					diff_img_path = '../snapshot/change/{}'.format(diff_img_name)

					changed = compare_img(t, old_snapshot_path, new_snapshot_path, diff_img_path)
					if changed:
						logger.info('[Task {}] Notify change'.format(t.id))
						notify_change('{} changed'.format(t.name), t.url, diff_img_path, diff_img_name)
				else:
					logger.info('[Task {}] No previous snapshot.'.format(t.id))

	except Exception as e:
		logger.exception(e)
		logger.error('[Task {}] Failed'.format(t.id))

	# break
session.commit()
close_driver()


