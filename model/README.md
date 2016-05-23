# Votes Models #

These Python files define the models for the Votes application.

## User ##

A user is a Google Account that can _vote_ on a _poll_ during a _meeting_. Attendance is taken at the beginning of a meeting and they can vote based on whether or not they are there. This is configurable in `vote.py` in the `can_user_vote()` method.

## Meeting ##

A meeting is a period of time in which people vote. The meeting begins with the secretary taking attendance. Then the secretary can open up a vote. It has the following properties:

- _start_ : time at which the meeting was opened. It is a DateTimeProperty.
- _closed_ : is the meeting open? Only one meeting can be opened at a time. It is a BooleanProperty.
- _present_: list of users present at the meetings. Repeated values of type StringProperty.
- _excused_: list of users excused at the meetings. Repeated values of type StringProperty.
- _unexcused_: list of users unexcused at the meetings. Repeated values of type StringProperty.

## Poll ##

## Vote ##
