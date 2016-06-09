import logging
import poll as Poll

from google.appengine.ext import ndb

'''
This is an in memory cache of votes
'''

class Vote(ndb.Model):
	#who voteds email
	user = ndb.StringProperty(required = True)
	#vote
	vote = ndb.IntegerProperty(required = True)
	#When the vote occured
	when = ndb.DateTimeProperty(auto_now_add = True)


#Dictionary
USER_VOTES = {}

def insert_or_update_user(user2, vote2):
	result = Vote.query(Vote.user == user2).get()
	if result is None:
		#Copy it to DB
		new_vote = Vote(user=user2, vote=int(vote2))
		new_vote.put()
	else:
		result.vote = int(vote2)
		result.put()

#Actually Vote
def vote(user, vote):
	if can_user_vote(user):
		#Log Vote
		logging.error('{} voted {}'.format(user,vote))
		#Set it in the cache
		#USER_VOTES[user] = vote
		new_vote = Vote(user = user, vote = int(vote))
		new_vote.put()


		return True
	else:
		#Log Vote
		logging.error('{} unable to cast vote.'.format(user))
		return False

def reset_vote():
	USER_VOTES.clear()
	#Drop the database
	ndb.delete_multi(Vote.query().fetch(keys_only = True))

def commit_votes():
	poll = Poll.get_open_polls_query().get()
	if poll is None:
		return
	results = get_votes()
	poll.votes_yes = results.get('yes')
	poll.votes_no = results.get('no')
	poll.votes_abstain = results.get('abstain')
	poll.put()

def get_votes():
	logging.error('get_votes()')
	yes = 0
	no = 0
	abstain = 0
	for vote in Vote.query().fetch():
		if vote.user in USER_VOTES:
			if USER_VOTES[vote.user].when < vote.when:
				USER_VOTES[vote.user] = vote.vote
		else:
			USER_VOTES[vote.user] = vote.vote
	for key,value in USER_VOTES.items():
		logging.error('User: {} voted: {}'.format(key, value))
		if int(value) == 0:
			yes += 1
		elif int(value) == 1:
			no += 1
		elif int(value) == 2:
			abstain += 1
	return {'yes':yes,'no':no, 'abstain':abstain, 'votes':len(USER_VOTES)}

#Can a certain user vote
#TODO: Check with active people at meeting
def can_user_vote(user):
	return True
