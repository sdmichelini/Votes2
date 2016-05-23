import webapp2
import jinja2
import json
import logging
import model.poll as poll
import model.meeting as meeting
import os

from google.appengine.api import users
from google.appengine.api import taskqueue

#Configure Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'view')),
		extensions=['jinja2.ext.autoescape'],
		autoescape=True)
#Main Page Handler

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = { 'polls':poll.find_open_polls_as_list(), 'logout':users.create_logout_url('/') }
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class AjaxPollHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(poll.find_open_polls_as_json())
	def put(self):
		self.response.headers['Content-Type'] = 'application/json'
		try:
			process_vote(json.loads(self.request.body))
			msg = {'message':'Voted.'}
		except NameError as error:
			self.response.set_status(400)
			msg = {'message':error.message}
		self.response.write(json.dumps(msg))

class OpenPollHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(poll.get_last_results(5)))

class OpenMeetingHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(meeting.find_open_meeting_json())

'''
Process the user's vote. Needs access to the actual vote and the users email. They should be logged in already
so users.get_current_user() should succeed.
'''
def process_vote(request_body):
	if 'vote' in request_body:
		if(request_body.get('vote') == 'Y'):
			vote = 0
		elif (request_body.get('vote') == 'N'):
			vote = 1
		elif (request_body.get('vote') == 'A'):
			vote = 2
		else:
			logging.error('Invalid Vote: {}'.format(request_body.get('vote')))
			raise NameError('Invalid Vote.')
		#Add to the taskqueue
		task = taskqueue.add(url='/worker/process_vote',
							target='worker',
							params={'user':users.get_current_user().email(),
									'vote':vote})
	else:
		raise NameError('No Vote Found.')

app = webapp2.WSGIApplication([
	('/',MainPage),
	('/api/poll',AjaxPollHandler),
	('/api/polls',OpenPollHandler),
	('/api/meeting',OpenMeetingHandler)
],debug=True)
