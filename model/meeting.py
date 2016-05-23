from google.appengine.ext import ndb
import json
import datetime
import logging
from time import mktime

OPEN_MEETING_CACHE = {}
OPEN_MEETING_KEY = 'open'

class DateJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if(isinstance(obj, datetime.datetime)):
			return int(mktime(obj.timetuple()))
		return json.JSONEncoder.default(self, obj)

class Meeting(ndb.Model):
	start = ndb.DateTimeProperty(auto_now = True)
	closed = ndb.BooleanProperty(default = False)
	present = ndb.StringProperty(repeated= True)
	excused = ndb.StringProperty(repeated = True)
	unexcused = ndb.StringProperty(repeated = True)

def find_open_meeting_query():
	#logging.error('DB Hit: find_open_meeting_query()')
	return Meeting.query().filter(Meeting.closed == False)

#Basically Return the NDB Object
def find_open_meeting_object(update = False):
	if not update and OPEN_MEETING_KEY in OPEN_MEETING_CACHE:
		result = OPEN_MEETING_CACHE[OPEN_MEETING_KEY]
	else:
		result = find_open_meeting_query().get()
		OPEN_MEETING_CACHE[OPEN_MEETING_KEY] = result
	return result

def find_open_meeting_json():
	return json.dumps(find_open_meeting_object(), cls=DateJsonEncoder)

def is_user_present(email):
	return (email in find_open_meeting_object().present)

def is_meeting_open(update = False):
	return (find_open_meeting_object(update) is not None)
def open_meeting():
	if find_open_meeting_object() is None:
		meeting = Meeting()
		meeting.put(use_cache=False, use_memcache=False)
		OPEN_MEETING_CACHE.clear()
	else:
		raise IOError('Meeting already opened.')

def close_current_meeting():
	#logging.error('close_current_meeting')
	open_meeting = find_open_meeting_object()
	if open_meeting is None:
		raise IOError('No meeting is open.')
	else:
		open_meeting.closed = True
		open_meeting.put(use_cache=False, use_memcache=False)
		clear_cache()

def clear_cache():
	OPEN_MEETING_CACHE.clear()

def take_attendence(present, excused, unexcused):
	meeting = find_open_meeting_object()
	if meeting is None:
		raise IOError('No meeting is open.')
	else:
		meeting.present = present
		meeting.excused = excused
		meeting.unexcused = unexcused
		meeting.put(use_cache=False, use_memcache=False)
		OPEN_MEETING_CACHE.clear()
