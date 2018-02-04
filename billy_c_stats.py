import asyncio
import pickle
import sqlite3
from datetime import datetime, timedelta

import billy_shared as sh

# Placeholder string
NOT_FOUND = "[nie znaleziono]"

# Open database
stats = sqlite3.connect(sh.file_path("billy_stats.db"))
stats_c = stats.cursor()

# Init database if necessary
stats_c.execute('''CREATE TABLE IF NOT EXISTS messages (
	message INTEGER NOT NULL PRIMARY KEY UNIQUE,
	server INTEGER NOT NULL,
	channel INTEGER,
	user INTEGER NOT NULL,
	time INTEGER NOT NULL,
	everyone INTEGER NOT NULL,
	deleted INTEGER NOT NULL,
	bot INTEGER NOT NULL,
	function TEXT
)''')
stats_c.execute('''CREATE TABLE IF NOT EXISTS emojis (
	emoji TEXT NOT NULL,
	server INTEGER NOT NULL,
	channel INTEGER,
	message INTEGER NOT NULL,
	user INTEGER NOT NULL,
	time INTEGER NOT NULL,
	count INTEGER NOT NULL,
	reaction INTEGER NOT NULL,
	custom INTEGER NOT NULL,
	bot INTEGER NOT NULL
)''')
stats.commit()

# Writing into database

def insert_msg(msg):
	data = (msg.id, msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.author.id, msg.timestamp, msg.mention_everyone, 0, 1 if msg.author.bot else 0, None)
	
	stats_c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	stats.commit()
	
	sh.debug("Inserted message {} into the stat database".format(msg.id))

def update_msg_function(msg, funct):
	data = (funct, msg.id)
	
	stats_c.execute("UPDATE messages SET function = ? WHERE message = ?", data)
	stats.commit()
	
	sh.debug("Updated message function: {}".format(funct))

def update_msg_deletion(msg):
	data = (msg.id, )
	
	stats_c.execute("UPDATE messages SET deleted = 1 WHERE message = ? LIMIT 1", data)
	remove_emojis(msg, True)
	
	sh.debug("Deleted message {} from the stat database".format(msg.id))

def insert_emojis_post(msg, emojis, customs, edited=False):
	if edited:
		remove_emojis(msg)
	
	if len(emojis+customs) == 0:
		return
	
	emojis_ready = {}
	
	for e in emojis:
		if e in emojis_ready:
			emojis_ready[e]["count"] += 1
		else:
			emojis_ready[e] = {}
			emojis_ready[e]["name"] = e
			emojis_ready[e]["custom"] = 0
			emojis_ready[e]["count"] = 1
			
	for e in customs:
		if e in emojis_ready:
			emojis_ready[e]["count"] += 1
		else:
			emojis_ready[e] = {}
			emojis_ready[e]["name"] = e
			emojis_ready[e]["custom"] = 1
			emojis_ready[e]["count"] = 1
	
	for e in emojis_ready.values():
		data = (e["name"], msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, msg.author.id, msg.timestamp, e["count"], 0, e["custom"], 1 if msg.author.bot else 0)
		stats_c.execute("INSERT INTO emojis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	
	stats.commit()

def insert_emojis_reaction(msg, user, emoji, custom):
	data = (emoji if not custom else str(emoji), msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, user.id, msg.timestamp, 1, 1, 1 if custom else 0, 1 if user.bot else 0)
	
	stats_c.execute("INSERT INTO emojis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	stats.commit()

def remove_reaction(msg, user, emoji, custom):
	data = (emoji if not custom else str(emoji), msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, user.id, msg.timestamp, 1, 1, 1 if custom else 0, 1 if user.bot else 0)
	
	stats_c.execute("DELETE FROM emojis WHERE emoji = ? AND server = ? AND channel = ? AND message = ? AND user = ? AND time = ? AND count = ? AND reaction = ? AND custom = ? AND bot = ? LIMIT 1", data)
	stats.commit()

def remove_emojis(msg, all=False):
	data = (msg.id, )
	
	if not all:
		query = "AND reaction = 0"
	else:
		query = ""
	
	stats_c.execute("DELETE FROM emojis WHERE message = ? {}".format(query), data)
	stats.commit()

# Helper functions

def prepare_conditions(time=None, channel=None, user=None, bot=False):
	conditions = ""
	
	if time == "yesterday":
		yesterday = datetime.now() - timedelta(days=-1)
		conditions += "AND date(time, 'localtime') = '{}' ".format(yesterday.strftime('%Y-%m-%d'))
	elif time == "today":
		yesterday = datetime.now() - timedelta(days=0)
		conditions += "AND date(time, 'localtime') = '{}' ".format(yesterday.strftime('%Y-%m-%d'))
	elif time != None:
		conditions += "AND date(time, 'localtime') = '{}' ".format(time)
	
	if not bot:
		conditions += "AND bot = 0 "
	
	return conditions

# Generating stats

def stats_users(client, server, rows=5, time=None, channel=None, user=None, bot=True, deleted=False):
	params = (server, rows)
	server_obj = client.get_server(server)
	conditions = prepare_conditions(time, channel, user, bot)
	ret = ""
	
	if not server:
		return "Coś skopałeś z ID serwera"
	
	if not deleted:
		conditions += "AND deleted = 0 "
	
	i = 1
	for row in stats_c.execute("SELECT user, count(*) AS result FROM messages WHERE server = ? {} GROUP BY user ORDER BY result DESC, user ASC LIMIT 0,?".format(conditions), params):
		user = server_obj.get_member(str(row[0]))
		ret += "#{}: {} ({})\n".format(i, user.display_name if user is not None else not_found, row[1])
		i += 1
	
	return ret.strip()

def stats_channels(client, server, rows=5, time=None, channel=None, user=None, bot=False, deleted=False):
	params = (server, rows)
	server_obj = client.get_server(server)
	conditions = prepare_conditions(time, channel, user, bot)
	ret = ""
	
	if not server:
		return "Coś skopałeś z ID serwera"
	
	if not deleted:
		conditions += "AND deleted = 0 "
	
	i = 1
	for row in stats_c.execute("SELECT channel, count(*) AS result FROM messages WHERE server = ? {} AND channel != 326696245684862987 GROUP BY channel ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions), params):
		channel = server_obj.get_channel(str(row[0]))
		ret += "#{}: {} ({})\n".format(i, channel.name if channel is not None else not_found, row[1])
		i += 1
	
	return ret.strip()

def stats_emojis(client, server, rows=5, time=None, channel=None, user=None, bot=False, custom_only=False):
	params = (server, rows)
	server_obj = client.get_server(server)
	conditions = prepare_conditions(time, channel, user, bot)
	ret = ""
	
	if not server:
		return "Coś skopałeś z ID serwera"
	
	if custom_only:
		conditions += "AND custom = 1 "
	
	i = 1
	for row in stats_c.execute("SELECT emoji, sum(count) AS result FROM emojis WHERE server = ? {} GROUP BY emoji ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions), params):
		ret += "#{}: {} ({})\n".format(i, row[0], row[1])
		i += 1
	
	return ret.strip()

# Commands

@asyncio.coroutine
def c_stats(client, message):
	is_private = str(message.channel).startswith("Direct Message")
	if is_private:
		yield from client.send_message(message.channel, "Po cholerę ci statystyki z priva?")
		return
	
	bot_stats = "bot" in sh.get_command(message).lower()
	bot_query = "AND function IS NOT NULL" if bot_stats else ""
	not_found = "[nie znaleziono]"
	
	server_id = message.server.id if message.server is not None else 0
	stat_limit = 15 if (is_private or str(message.channel) in ["japabocie", "japa_bocie"]) else 5
	
	params = (server_id, stat_limit)
	
	ret = ("Ludzie, którzy nadużywają bota na tym serwerze:\n\n" if bot_stats else "Najwięksi spamerzy na tym serwerze:\n\n")
	
	i = 1
	for row in stats_c.execute("SELECT user, count(*) AS result FROM messages WHERE server = ? {} GROUP BY user ORDER BY result DESC, user ASC LIMIT 0,?".format(bot_query), params):
		user = message.server.get_member(str(row[0]))
		ret += "#{}: {} ({})\n".format(i, user.display_name if user is not None else not_found, row[1])
		i += 1
	
	ret += "\nNajbardziej zaspamowane kanały:\n\n"
	
	i = 1
	for row in stats_c.execute("SELECT channel, count(*) AS result FROM messages WHERE server = ? {} GROUP BY channel ORDER BY result DESC, channel ASC LIMIT 0,?".format(bot_query), params):
		ch_id = str(row[0]) if row[0] not in [326696245684862987] else "0"
		channel = message.server.get_channel(ch_id)
		ret += "#{}: {} ({})\n".format(i, channel.name if channel is not None else not_found, row[1])
		i += 1
	
	if bot_stats:
		ret += "\nNajczęściej używane funkcje:\n\n"
		
		i = 1
		for row in stats_c.execute("SELECT function, count(*) AS result FROM messages WHERE server = ? {} GROUP BY function ORDER BY result DESC, function ASC LIMIT 0,?".format(bot_query), params):
			ret += "#{}: {} ({})\n".format(i, row[0], row[1])
			i += 1
	
	yield from client.send_message(message.channel, ret.strip())

c_stats.command = r"(bot|stat)(s|ystyki)?"
c_stats.desc = "hidden"

# Test command

@asyncio.coroutine
def c_stattest(client, message):
	yesterday = (datetime.now() - timedelta(days=0)).strftime('%Y-%m-%d')
	
	ret = "Statystyki za dzień {}\n\nLiczba wysłanych wiadomości:\n".format(yesterday)
	
	ret += stats_users(client, "174449535811190785", rows=10, time=yesterday)
	ret += "\n\nNajbardziej aktywne kanały:\n"
	ret += stats_channels(client, "174449535811190785", rows=10, time=yesterday)
	ret += "\n\nNajczęściej używane emoty:\n"
	ret += stats_emojis(client, "174449535811190785", rows=10, time=yesterday, custom_only=True)
	
	yield from client.send_message(message.channel, ret)

c_stattest.command = r"stattest"
c_stattest.desc = "hidden"

# Daily stats

@asyncio.coroutine
def t_daily_stats(client, channels):
	yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
	
	ret = "Statystyki za dzień {}\n\nLiczba wysłanych wiadomości:\n".format(yesterday)
	
	ret += stats_users(client, "174449535811190785", rows=10, time=yesterday)
	ret += "\n\nNajbardziej aktywne kanały:\n"
	ret += stats_channels(client, "174449535811190785", rows=10, time=yesterday)
	ret += "\n\nNajczęściej używane emoty:\n"
	ret += stats_emojis(client, "174449535811190785", rows=10, time=yesterday, custom_only=True)
	
	for ch in channels:
		yield from client.send_message(ch, ret)

t_daily_stats.channels = ["174449535811190785"]
t_daily_stats.time = "00:01"