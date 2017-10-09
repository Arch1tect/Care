# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime

from db.model import CareTask, TaskLog
from db_session import session
from snapshot import take_snapshot, close_driver
from image_diff import compare_img
from mailgun import notify_change
import setup

logger = logging.getLogger(__name__)


for t in session.query(CareTask).all():
	now = datetime.utcnow()
	new_snapshot_taken = False
	try:
		time_past = (now-t.last_run_time).total_seconds()

		if time_past >= t.interval:
			check_log = TaskLog(task_id=t.id, timestamp=now, success=False)
			try:
				logger.info('[Task {}] last_run_time {}'.format(t.id, t.last_run_time))

				# get new snapshot
				old_snapshot_path = '../snapshot/{}-{}.png'.format(t.id, t.last_run_id)
				new_snapshot_name = '{}-{}.png'.format(t.id, t.last_run_id + 1)
				new_snapshot_path = '../snapshot/{}'.format(new_snapshot_name)
			
				new_snapshot_taken = take_snapshot(t, new_snapshot_path)
				
				if new_snapshot_taken:

					t.last_run_id = t.last_run_id + 1
					t.last_run_time = now
					# ensure there's a previous snapshot to compare
					if os.path.isfile(old_snapshot_path):
						# compare new snapshot with old snapshot
						diff_img_name = '{}-{}.png'.format(t.id, t.last_run_id+1)
						diff_img_path = '../snapshot/change/{}'.format(diff_img_name)

						changed = compare_img(t, old_snapshot_path, new_snapshot_path, diff_img_path)
						check_log.changed = changed
						if changed:
							logger.info('[Task {}] Notify change'.format(t.id))
							task_name = t.name
							if not task_name:
								task_name = t.url
							email_subject = '{} changed'.format(task_name)
							notify_change(email_subject, t.url, diff_img_path, diff_img_name)

					else:
						logger.info('[Task {}] No previous snapshot.'.format(t.id))
					check_log.success = True
			except Exception as e:
				logger.exception(e)
				logger.error('[Task {}] fail to check update'.format(t.id))
			session.add(check_log)

	except Exception as e:
		logger.exception(e)
		logger.error('[Task {}] fail to check time past'.format(t.id))

session.commit()
# close_driver()


