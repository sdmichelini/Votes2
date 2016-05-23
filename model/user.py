from google.appengine.ext import ndb
import json
import datetime
import logging
import base64

USER_CACHE = {}
ALL_KEY = 'all'

'''This is basically a wrapper around a user from Google Accounts.
This is meant to enfore attendence for meetings and voting. This is preventing every Google Accounts USer
from Voting in the App. The Admin will Have to Manually Add Users to the Application
'''
class VotingUser(ndb.Model):
	email = ndb.StringProperty(required = True)
	active = ndb.BooleanProperty(default = False)
	grad_year = ndb.IntegerProperty(required = True)
	name = ndb.StringProperty(required = True)
	@classmethod
	def get_by_user(cls, user):
		return cls.query().filter(cls.email == user.email()).get()
	@classmethod
	def query_by_email(cls, email):
		return cls.query().filter(cls.email == email)

def add_user(new_email, grad_year, name):
	logging.error('Added User w/ Name: {} Grad Year: {} and Email: {}'.format(name, grad_year, new_email))
	#Query Current Users for New User Id
	query = VotingUser.query_by_email(new_email)
	results = query.fetch(1)
	if len(results) < 1:
		new_user = VotingUser(email=new_email, grad_year=int(grad_year), name=name)
		new_user.put()
		#Invalidate the Cache
		USER_CACHE.clear()
		return True
	else:
		return False

def activate_user(new_email):
	#Activate NDB User
	#Query Current Users for New User Id
	query = VotingUser.query_by_email(new_email)
	results = query.fetch(1)
	if len(results) < 1:
		return False
	else:
		db_user = results[0]
		db_user.active = True
		db_user.put()
		return True

def get_users_as_json():
	return json.dumps(get_users_as_list())

def get_users_as_list():
	#Get all the Users
	if ALL_KEY not in USER_CACHE:
		logging.error('DB Hit: get_users_as_list()')
		query = VotingUser.query()
		results = query.fetch()
		ret = list()
		for r in results:
			dic = r.to_dict()
			dic['encode'] = base64.b64encode(dic['email'])
			ret.append(dic)
		#ret = list([r.to_dict() for r in results])
		USER_CACHE[ALL_KEY] = ret
	else:
		ret = USER_CACHE[ALL_KEY]
	return ret

def delete_user(new_email):
	#Query Current Users for New User Id
	query = VotingUser.query_by_email(new_email)
	results = query.fetch(1)
	if len(results) < 1:
		return False
	else:
		results[0].key.delete()
		return True
