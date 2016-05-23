import webapp2
import jinja2
import json


import model.poll as poll
import model.user as user
import model.vote as vote
import model.meeting as meeting
import google.appengine.api
import os
import logging
from google.appengine.ext.db import BadValueError

#Configure Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'view')),
		extensions=['jinja2.ext.autoescape'],
		autoescape=True)



#Main Admin Page Handler
class AdminLandingPage(webapp2.RequestHandler):
	def get(self):
		template_values = { 'meeting_open': meeting.is_meeting_open() }

		template = JINJA_ENVIRONMENT.get_template('admin.html')
		self.response.write(template.render(template_values))

class AdminNewPollHandler(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		try:
			data = json.loads(self.request.body)
			pol = process_new_poll(data)
			if pol == None:
				raise NameError('Too Many Polls Open')
			msg = {
				'message':'Poll Created',
				'title':pol.title,
				'description':pol.description
			}
			vote.reset_vote()
			self.response.set_status(201)
		except (ValueError, BadValueError) as e:
			self.response.set_status(400)
			msg = {
				'message':'Error: Could Not Parse Request'
			}
		except NameError:
			self.response.set_status(409)
			msg = {
				'message':'Error: Too Many Polls Open'
			}
		self.response.write(json.dumps(msg))
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(poll.get_last_results(5)))
	def delete(self):
		self.response.headers['Content-Type'] = 'application/json'
		msg = {
			'message':'Polls Closed'
		}
		vote.commit_votes()
		poll.delete_open_polls()
		vote.reset_vote()
		self.response.write(json.dumps(msg))

class AdminUserHandler(webapp2.RequestHandler):
	def get(self):
		template_values = { 'users': user.get_users_as_list() }
		logging.error('{}'.format(user.get_users_as_json()))
		template = JINJA_ENVIRONMENT.get_template('admin_users.html')
		self.response.write(template.render(template_values))
	def delete(self):
		self.response.write('Error Not Implemented')
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		try:
			data = json.loads(self.request.body)
			results = process_new_user(data)
			msg = {
				'message':'Created New User.'
			}
			self.response.set_status(201)
		except ValueError:
			self.response.set_status(400)
			msg = {
				'message':'Unable to Parse Request.'
			}
		except BadValueError:
			self.response.set_status(400)
			msg = {
				'message':'Unable to Create Database Object.'
			}
		except NameError:
			self.response.set_status(400)
			msg = {
				'message':'Error. Invalid Request. All Fields Not Specified'
			}
		self.response.write(json.dumps(msg))

class AttendenceHandler(webapp2.RequestHandler):
	def get(self):
		#logging.error('{}'.format(user.get_users_as_json()))
		template_values = { 'users': user.get_users_as_list() }
		template = JINJA_ENVIRONMENT.get_template('attendence.html')
		self.response.write(template.render(template_values))
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		try:
			data = json.loads(self.request.body)
			present = data.get('present')
			if present is None:
				raise ValueError
			excused = data.get('excused')
			if excused is None:
				raise ValueError
			unexcused = data.get('unexcused')
			if unexcused is None:
				raise ValueError
			meeting.take_attendence(present, excused, unexcused)
			msg = {'message':'Successfully took attendence'}
		except ValueError:
			self.response.set_status(400)
			msg = {'message':'Could not parse JSON.'}
		except IOError:
			self.response.set_status(400)
			msg = {'message':'Meeting Not Open.'}
		self.response.write(json.dumps(msg))


class MeetingHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps({'meeting_open':meeting.is_meeting_open(True)}))
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		try:
			meeting.open_meeting()
			msg = {'message':'Meeting Created.'}
			self.response.set_status(201)
		except IOError:
			self.response.set_status(409)
			msg={'message':'Unable to Create Meeting.'}
		self.response.write(json.dumps(msg))
	def delete(self):
		self.response.headers['Content-Type'] = 'application/json'
		try:
			meeting.close_current_meeting()
			msg = {'message':'Meeting Closed.'}
			self.response.set_status(200)
		except IOError:
			self.response.set_status(409)
			msg={'message':'Unable to Close Meeting.'}
		self.response.write(json.dumps(msg))

# Process the Post Data
def process_new_poll(data):
	title = data.get('title')
	description = data.get('description')
	return poll.create_poll(title, description)

# Process New User
def process_new_user(data):
	val = user.add_user(data.get('email'), data.get('grad_year'), data.get('username'))
	if val == False:
		raise NameError('Cannot Add User')

app = webapp2.WSGIApplication([
	('/admin',AdminLandingPage),
	('/admin/attendence',AttendenceHandler),
	('/admin/poll',AdminNewPollHandler),
	('/admin/users',AdminUserHandler),
	('/admin/meetings',MeetingHandler)
],debug=True)
