from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
import json
from time import mktime
import datetime

import logging

#Cache
OPEN_POLL_CACHE = {}
OPEN_KEY = 'open'

class DateJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if(isinstance(obj, datetime.datetime)):
			return int(mktime(obj.timetuple()))
		return json.JSONEncoder.default(self, obj)

class Poll(ndb.Model):
	title = ndb.StringProperty(required=True)
	description = ndb.StringProperty(required=True)
	votes_yes = ndb.IntegerProperty(default = 0)
	votes_no = ndb.IntegerProperty(default = 0)
	votes_abstain = ndb.IntegerProperty(default = 0)
	time = ndb.DateTimeProperty(auto_now=True)
	closed = ndb.BooleanProperty(default=False)

def get_last_results(amount):
	return list([p.to_dict() for p in Poll.query().order(-Poll.time).fetch(amount, projection=[Poll.title, Poll.votes_yes, Poll.votes_no, Poll.votes_abstain])])

def create_poll(title, description):
	#Can't Create the Poll
	if len(find_open_polls_as_list()) > 0:
		return None
	poll = Poll(title=title, description=description)
	poll.put()
	OPEN_POLL_CACHE.clear()
	return poll

def get_open_polls_query():
	return Poll.query().filter(Poll.closed == False)

def find_open_polls():
	logging.error('DB Hit: find_open_polls()')
	return get_open_polls_query().fetch(projection=[Poll.title, Poll.description])

def find_last_polls(num):
	logging.debug('Finding Last {} Polls'.format(num))

def delete_open_polls():
	polls = get_open_polls_query().fetch()
	for poll in polls:
		poll.closed = True
		poll.put()
	OPEN_POLL_CACHE.clear()

def find_open_polls_as_list():
	if OPEN_KEY in OPEN_POLL_CACHE:
		ret = OPEN_POLL_CACHE[OPEN_KEY]
	else:
		ret = list([p.to_dict() for p in find_open_polls()])
		OPEN_POLL_CACHE[OPEN_KEY] = ret
	return ret
#Get Json
def find_open_polls_as_json():
	return json.dumps(find_open_polls_as_list(), cls=DateJsonEncoder)
