import sys
sys.path.insert(1,'/usr/local/google_appengine')
sys.path.insert(1,'/usr/local/google_appengine/lib/yaml/lib')

import unittest



from model import meeting
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class MeetingTestCase(unittest.TestCase):

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		ndb.get_context().clear_cache()
		ndb.get_context().set_cache_policy(False)

	def tearDown(self):
		meeting.clear_cache()
		self.testbed.deactivate()

	def testOpenMeeting(self):
		meeting.open_meeting()
		self.assertEqual(1, len(meeting.Meeting.query().fetch(2)))

	def testFindMeeting(self):
		#There should be no meeting initially
		result = meeting.find_open_meeting_object(True)
		self.assertEqual(None, result)
		#Open a meeting
		meeting.open_meeting()
		#Find the Meeting
		result = meeting.find_open_meeting_object(True)
		self.assertNotEqual(None,result)

	def testCloseMeeting(self):
		#Open a Meeting
		meeting.open_meeting()
		#Close it
		meeting.close_current_meeting()
		#Should be No Meetings
		result = meeting.find_open_meeting_object(True)
		self.assertEqual(None, result)

	def testAttendence(self):
		#Open a Meeting
		meeting.open_meeting()
		present = ['test1', 'test2', 'test3']
		excused = ['test4', 'test5', 'test6']
		unexcused = ['test11', 'test12', 'test13']
		meeting.take_attendence(present,excused,unexcused)
		#get the meeting
		result = meeting.Meeting.query().get()
		self.assertNotEqual(None, result)
		self.assertEqual(present, result.present)
		self.assertEqual(excused, result.excused)
		self.assertEqual(unexcused, result.unexcused)

	def testIsMeetingOpen(self):
		self.assertFalse(meeting.is_meeting_open(True))
		meeting.open_meeting()
		self.assertTrue(meeting.is_meeting_open(True))

if __name__ =='__main__':
	unittest.main()
