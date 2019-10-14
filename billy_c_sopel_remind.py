# coding=utf-8
"""
remind.py - Sopel Reminder Module
Copyright 2011, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import os
import re
import time
import threading
import collections
import codecs
from datetime import datetime
#from sopel.module import commands, example, NOLIMIT
NOLIMIT = 1
#import sopel.tools
from billy_sopel_time import get_timezone, format_time

import billy_shared as sh
import asyncio
import discord
import math

try:
	import pytz
except:
	pytz = None


def filename():
	return sh.file_path("billy_db_reminders.db")


def load_database(name):
	data = {}
	if os.path.isfile(name):
		f = codecs.open(name, 'r', encoding='utf-8')
		for line in f:
			unixtime, channel, nick, message = line.split('\t')
			message = message.rstrip('\n')
			t = int(float(unixtime))  # WTFs going on here?
			reminder = (channel, nick, message)
			try:
				data[t].append(reminder)
			except KeyError:
				data[t] = [reminder]
		f.close()
	return data


def dump_database(name, data):
	f = codecs.open(name, 'w', encoding='utf-8')
	for unixtime, reminders in dict.items(data):
		for channel, nick, message in reminders:
			f.write('%s\t%s\t%s\t%s\n' % (unixtime, channel, nick, message))
	f.close()


@asyncio.coroutine
def setup(client):
	client.rfn = filename()
	client.rdb = load_database(client.rfn)
	
	@asyncio.coroutine
	def monitor(client):
		yield from client.wait_until_ready()
		
		yield from asyncio.sleep(5)
		
		while not client.is_closed:
			now = int(time.time())
			unixtimes = [int(key) for key in client.rdb]
			oldtimes = [t for t in unixtimes if t <= now]
			if oldtimes:
				for oldtime in oldtimes:
					for (channel, nick, message) in client.rdb[oldtime]:
						if message:
							yield from client.send_message(discord.Object(id=channel), "[przypomnienie] " + nick + ': ' + message)
						else:
							yield from client.send_message(discord.Object(id=channel), "[przypomnienie] " + nick + '!')
					del client.rdb[oldtime]
				dump_database(client.rfn, client.rdb)
			
			yield from asyncio.sleep(2.5)
	
	client.loop.create_task((yield from monitor(client)))


scaling = collections.OrderedDict([
	('years', 365 * 24 * 3600),
	('year', 365 * 24 * 3600),
	('yrs', 365 * 24 * 3600),
	('y', 365 * 24 * 3600),
	
	('lata', 365 * 24 * 3600),
	('lat', 365 * 24 * 3600),
	('rok', 365 * 24 * 3600),
	('r\.', 365 * 24 * 3600),
	('r', 365 * 24 * 3600),

	('months', 30 * 24 * 3600),
	('month', 30 * 24 * 3600),
	('mo', 30 * 24 * 3600),
	
	('miesięcy', 30 * 24 * 3600),
	('miesiące', 30 * 24 * 3600),
	('miesiąc', 30 * 24 * 3600),
	('miesiecy', 30 * 24 * 3600),
	('miesiace', 30 * 24 * 3600),
	('miesiac', 30 * 24 * 3600),
	('mies\.', 30 * 24 * 3600),

	('weeks', 7 * 24 * 3600),
	('week', 7 * 24 * 3600),
	('wks', 7 * 24 * 3600),
	('wk', 7 * 24 * 3600),
	('w', 7 * 24 * 3600),

	('tydzień', 7 * 24 * 3600),
	('tygodnie', 7 * 24 * 3600),
	('tygodni', 7 * 24 * 3600),
	('tydzien', 7 * 24 * 3600),
	('tyg\.', 7 * 24 * 3600),
	('tyg', 7 * 24 * 3600),

	('days', 24 * 3600),
	('day', 24 * 3600),
	('dzień', 24 * 3600),
	('dzien', 24 * 3600),
	('dni', 24 * 3600),
	('d\.', 24 * 3600),
	('d', 24 * 3600),

	('hours', 3600),
	('hour', 3600),
	('hrs', 3600),
	('hr', 3600),
	('h\.', 3600),
	('h', 3600),

	('godziny', 3600),
	('godzinę', 3600),
	('godzine', 3600),
	('godzin', 3600),

	('minutes', 60),
	('minute', 60),
	('minuty', 60),
	('minutę', 60),
	('minut', 60),
	('mins', 60),
	('min\.', 60),
	('min', 60),
	('m\.', 60),
	('m', 60),


	('seconds', 1),
	('second', 1),
	('sekundy', 1),
	('sekunde', 1),
	('sekundę', 1),
	('secs', 1),
	('sec', 1),
	('sek\.', 1),
	('sek', 1),
	('s\.', 1),
	('s', 1),

])

periods = '|'.join(scaling.keys())


@asyncio.coroutine
def c_remind(client, message_obj):
	"""Gives you a reminder in the given amount of time."""
	if not sh.get_args(message_obj):
		#yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "no i?")
		return NOLIMIT
	if len(sh.get_args(message_obj).split(" ")) < 2:
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "ale o czym mam przypomnieć?")
		return NOLIMIT
	duration = 0
	message = filter(None, re.split('(\d+(?:\.\d+)? ?(?:(?i)' + periods + ')) ?',
									sh.get_args(message_obj))[1:])
	reminder = ''
	stop = False
	for piece in message:
		grp = re.match('(\d+(?:\.\d+)?) ?(.*) ?', piece)
		if grp and not stop:
			length = float(grp.group(1))
			factor = scaling.get(grp.group(2).lower(), 60)
			duration += length * factor
		else:
			reminder = reminder + piece
			stop = True
	if duration == 0:
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "i może frytki do tego?")
		return

	if duration % 1:
		duration = int(duration) + 1
	else:
		duration = int(duration)
	timezone = get_timezone(
		None, None, None, message_obj.author.mention, message_obj.channel.id)
	yield from create_reminder(client, message_obj, duration, reminder, timezone)

c_remind.command = r"(za|in)"
c_remind.params = ["za ile czasu", "wiadomość"]
c_remind.desc = "Przypomnij za..."


@asyncio.coroutine
def c_at(client, message_obj):
	"""
	Gives you a reminder at the given time. Takes hh:mm:ssTimezone
	message. Timezone is any timezone Sopel takes elsewhere; the best choices
	are those from the tzdb; a list of valid options is available at
	http://sopel.chat/tz . The seconds and timezone are optional.
	"""
	if not sh.get_args(message_obj):
		#yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "no i?")
		return NOLIMIT
	if len(sh.get_args(message_obj).split(" ")) < 2:
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "ale o czym mam przypomnieć?")
		return NOLIMIT
	regex = re.compile(r'(?:(\d{4})-(\d{1,2})-(\d{1,2}) )?(\d+):(\d+)(?::(\d+))?([^\s\d]+)? (.*)')
	match = regex.match(sh.get_args(message_obj))
	if not match:
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "i może frytki do tego?")
		return NOLIMIT
	year, month, day, hour, minute, second, tz, message = match.groups()
	if not second:
		second = '0'

	# if pytz:
		# timezone = get_timezone(None, None, tz,
								# message_obj.author.mention, message_obj.channel.id)
		# if not timezone:
			# timezone = 'UTC'
		# now = datetime.now(pytz.timezone(timezone))
		# at_time = datetime(now.year, now.month, now.day,
						   # sorted((0, int(hour), 23))[1], sorted((0, int(minute), 59))[1], sorted((0, int(second), 59))[1],
						   # tzinfo=now.tzinfo)
		# timediff = at_time - now
	# else:
	if tz and tz.upper() != 'UTC':
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "nie znam się na strefach czasowych.")
		return NOLIMIT
	now = datetime.now()
	
	if not year:
		year = str(now.year)
	if not month:
		month = str(now.month)
	if not day:
		day = str(now.day)
	
	try:
		at_time = datetime(sorted((2018, int(year), 2036))[1], sorted((1, int(month), 12))[1], sorted((1, int(day), 31))[1],
					   sorted((0, int(hour), 23))[1], sorted((0, int(minute), 59))[1], sorted((0, int(second), 59))[1])
		timediff = at_time - now
		
		duration = math.floor(timediff.total_seconds())
		if duration < 0:
			duration += 86400
		
		if duration < 0:
			raise Exception()
	except:
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + "coś mi się nie podoba ta data/godzina.")
		return
	
	yield from create_reminder(client, message_obj, duration, message, 'UTC')

c_at.command = r"(o|at)"
c_at.params = ["YYYY-MM-DD", "HH:MM", "wiadomość"]
c_at.desc = "Przypomnij o..."


@asyncio.coroutine
def create_reminder(client, message_obj, duration, message, tz):
	t = int(time.time()) + duration
	reminder = (message_obj.channel.id, message_obj.author.mention, message)
	try:
		client.rdb[t].append(reminder)
	except KeyError:
		client.rdb[t] = [reminder]
	
	dump_database(client.rfn, client.rdb)
	
	if duration >= 60:
		remind_at = datetime.fromtimestamp(t)
		timef = format_time(None, None, tz, message_obj.author.mention,
							message_obj.channel.id, remind_at)
	
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + 'dobra, przypomnę w dniu %s' % timef)
	else:
		yield from client.send_message(message_obj.channel, sh.mention(message_obj) + 'dobra, przypomnę za %s sekund' % duration)
