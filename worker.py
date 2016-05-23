'''
This is the worker module for the votes task handler.
'''

from google.appengine.ext import ndb

import json
import logging
import model.poll as Poll
import model.vote as Vote
import webapp2

USER_VOTES = {}

#Called when there is a new vote
class VoteHandler(webapp2.RequestHandler):
	#Add a New Vote
	def post(self):
		#Person Who Voted
		user = self.request.get('user')
		#Their Vote
		vote = self.request.get('vote')
		#Vote in our cache
		Vote.vote(user,vote)

	def delete(self):
		self.response.headers['Content-Type'] = 'application/json'
		Vote.reset_vote()
		msg = {'message':'Votes Deleted'}
		self.response.write(json.dumps(msg))




app = webapp2.WSGIApplication([
	('/worker/process_vote', VoteHandler)
],debug = True)
