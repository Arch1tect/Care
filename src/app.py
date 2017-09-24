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

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level = logging.INFO
	)
logger = logging.getLogger(__name__)

db_url = 'chat-anywhere-mysql.cjwz9xnh80ai.us-west-1.rds.amazonaws.com'
connection_str = 'mysql://{}:{}@{}'.format(db_user, db_password, db_url)
engine = create_engine(connection_str)
engine.execute("USE care")
DBSession = sessionmaker(bind=engine)
session = DBSession()

for t in session.query(CareTask).all():
	now = datetime.utcnow()
	new_snapshot_taken = False
	try: 
		time_past = (now-t.last_run).total_seconds()
		# now_timestamp = int((now-datetime.utcfromtimestamp(0)).total_seconds())
		# last_run_timestamp = int((t.last_run-datetime.utcfromtimestamp(0)).total_seconds())
		if time_past >= t.interval:
			logger.info('[Task {}] Last_run {}'.format(t.id, t.last_run))

			# get new snapshot
			old_snapshot_name = '../snapshot/{}-{}.png'.format(t.id, t.run_count)
			snapshot_name = '../snapshot/{}-{}.png'.format(t.id, t.run_count + 1)
			
			# print old_snapshot_name
			take_snapshot(t, snapshot_name)
			new_snapshot_taken = True

			# ensure there's a previous snapshot to compare
			if os.path.isfile(old_snapshot_name):
				# compare new snapshot with old snapshot
				diff_img_path = '../snapshot/change/{}-{}.png'.format(t.id, t.run_count+1)

				changed = compare_img(t, old_snapshot_name, snapshot_name, diff_img_path)
				if changed:
					logger.info('[Task {}] Notify change'.format(t.id))
					notify_change('{} changed'.format(t.name), diff_img_path)
			else:
				logger.info('[Task {}] No previous snapshot.'.format(t.id))

	except Exception as e:
		logger.exception(e)
		logger.error('[Task {}] Failed'.format(t.id))
	if new_snapshot_taken:
		t.run_count = t.run_count + 1
		t.last_run = now
	# break
session.commit()
close_driver()


