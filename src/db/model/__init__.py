import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class CareTask(Base):
	__tablename__ = 'task'
	# Here we define columns for the table person
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	interval = Column(Integer)
	last_run_time = Column(TIMESTAMP)
	created = Column(TIMESTAMP, default=datetime.datetime.utcnow)
	url = Column(String(1000))
	last_run_id = Column(Integer)
	roi = Column(String(63))

class TaskLog(Base):
	__tablename__ = 'log'
	# Here we define columns for the table person
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	task_id = Column(Integer)
	timestamp = Column(TIMESTAMP)
	changed = Column(Boolean)
	success = Column(Boolean)
