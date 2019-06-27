import discord
import asyncio
import sqlite3
import re
import emoji
from datetime import datetime, timedelta
from discord.utils import find
from timeit import default_timer as timer

import billy_shared as sh

# Placeholder string
NOT_FOUND = "[nie znaleziono]"

# Channels to hide results from (they are still calculated!)
CHANNELS_TO_OMIT = str(tuple([326696245684862987, 425724173906870284, 471373220545691661])).rstrip(',)') + ')'

# Database init strings

MSG_INIT_STRING = '''CREATE TABLE IF NOT EXISTS messages (
	message INTEGER NOT NULL PRIMARY KEY UNIQUE,
	server INTEGER NOT NULL,
	channel INTEGER,
	user INTEGER NOT NULL,
	time INTEGER NOT NULL,
	everyone INTEGER NOT NULL,
	deleted INTEGER NOT NULL,
	bot INTEGER NOT NULL,
	function TEXT
)'''
EMO_INIT_STRING = '''CREATE TABLE IF NOT EXISTS emojis (
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
)'''

# Open database
stats = sqlite3.connect(sh.file_path("billy_db_stats.db"))
stats_c = stats.cursor()

# Init database if necessary
stats_c.execute(MSG_INIT_STRING)
stats_c.execute(EMO_INIT_STRING)
stats.commit()

# Writing into database

def insert_msg(msg, db=stats, cursor=stats_c, tmp=False):
	data = (msg.id, msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.author.id, msg.timestamp, msg.mention_everyone, 0, 1 if msg.author.bot else 0, None)
	
	cursor.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	if not tmp:
		db.commit()
	
	sh.debug("Inserted message {} into the stat database".format(msg.id))

def update_msg_function(msg, funct, db=stats, cursor=stats_c, tmp=False):
	data = (funct, msg.id)
	
	cursor.execute("UPDATE messages SET function = ? WHERE message = ?", data)
	if not tmp:
		db.commit()
	
	sh.debug("Updated message function: {}".format(funct))

def update_msg_deletion(msg, db=stats, cursor=stats_c):
	data = (msg.id, )
	
	cursor.execute("UPDATE messages SET deleted = 1 WHERE message = ? LIMIT 1", data)
	remove_emojis(msg, True)
	
	sh.debug("Deleted message {} from the stat database".format(msg.id))

def insert_emojis_post(msg, emojis, customs, edited=False, db=stats, cursor=stats_c, tmp=False):
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
		cursor.execute("INSERT INTO emojis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	
	if not tmp:
		db.commit()

def insert_emojis_reaction(msg, user, emoji, custom, db=stats, cursor=stats_c, tmp=False):
	data = (emoji if not custom else str(emoji), msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, user.id, msg.timestamp, 1, 1, 1 if custom else 0, 1 if user.bot else 0)
	
	cursor.execute("INSERT INTO emojis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	
	if not tmp:
		db.commit()

def remove_reaction(msg, user, emoji, custom, db=stats, cursor=stats_c):
	data = (emoji if not custom else str(emoji), msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, user.id, msg.timestamp, 1, 1, 1 if custom else 0, 1 if user.bot else 0)
	
	cursor.execute("DELETE FROM emojis WHERE emoji = ? AND server = ? AND channel = ? AND message = ? AND user = ? AND time = ? AND count = ? AND reaction = ? AND custom = ? AND bot = ? LIMIT 1", data)
	db.commit()

def remove_emojis(msg, all=False, db=stats, cursor=stats_c):
	data = (msg.id, )
	
	if not all:
		query = "AND reaction = 0"
	else:
		query = ""
	
	cursor.execute("DELETE FROM emojis WHERE message = ? {}".format(query), data)
	db.commit()

# Helper functions

def generate_date_format(date):
	return {
		1 : "%Y-%m",
		2 : "%Y-%m-%d"
	}.get(date.count("-"), "%Y")

def line_split(line):
	return re.findall(r'(\S+[=:](".+?"|\'.+?\'|\S+))', line)

def parse_stats_args(client, message, args):
	# Default values
	ret_array = {
		"server" : message.server.id if (message and message.server) else "0",
		"time" : None,
		"channel" : None,
		"user" : None,
		"bot" : False,
		"everyone" : False
	}
	
	# Argument name replacements
	repl_args = {
		"server" : r"serwer",
		"time" : r"czas|kiedy|when|data|date",
		"channel" : r"kana(l|ł)|gdzie|where",
		"user" : r"kto|auth?or|u(ż|z)ytkownik",
		"bot" : r"boty?"
	}
	
	# Value replacements
	repl_values = {
		"time" : {
			"today" : r"dzi(s|ś)|dzisiaj",
			"yesterday" : r"wczoraj",
			"last_month" : r"zesz(l|ł)y_?miesi(a|ą)c",
			"this_month" : r"ten_?miesi(a|ą)c",
			"month" : r"miesi(a|ą)c"
		},
		"channel" : {
			(message.channel.id if message else 0) : r"ten|tu(taj)?|this|here"
		},
		"user" : {
			(message.author.id if message else 0) : r"me|ja"
		},
		"bot" : {
			True : r"t|tak|y|yes|true|1",
			False : r"n|no|nie|f|false|0"
		},
		"everyone" : {
			True : r"t|tak|y|yes|true|1",
			False : r"n|no|nie|f|false|0"
		}
	}
	
	# Parsing each possible argument
	for arg in line_split(args):
		e = re.split("=|:", arg[0])
		
		if len(e) != 2:
			continue
		else:
			argument = e[0]
			value = e[1].strip('\'"')
			
			# Replace argument
			for k, v in repl_args.items():
				argument = re.sub("^"+v+"$", k, argument, flags=re.I)
			
			# Replace value
			if argument in repl_values:
				for k, v in repl_values[argument].items():
					value = re.sub("^"+v+"$", str(k), value, flags=re.I)
			
			# Convert to bool
			if argument in ["bot", "everyone"]:
						value = (value == "True")
			
			if argument in ret_array.keys():
				ret_array[argument] = value
	
	# Check if server exists
	if ret_array["server"] and not ret_array["server"].isdigit():
		e = find(lambda m: re.search(ret_array["server"], m.name, flags=re.I), client.servers)
		if e:
			ret_array["server"] = e.id
		else:
			ret_array["server"] = -1
	
	# Check if channel exists
	if ret_array["channel"] and not ret_array["channel"].isdigit():
		e = find(lambda m: re.search(ret_array["channel"], m.name, flags=re.I), client.get_all_channels())
		if e:
			ret_array["channel"] = e.id
		else:
			ret_array["channel"] = -1
	
	# Check if user exists
	if ret_array["user"] and not ret_array["user"].isdigit():
		e = find(lambda m: re.search(ret_array["user"], m.name, flags=re.I), client.get_all_members())
		if not e:
			e = find(lambda m: re.search(ret_array["user"], m.display_name, flags=re.I), client.get_all_members())
		
		if e:
			ret_array["user"] = e.id
		else:
			ret_array["user"] = -1
	
	# Handle errors
	ret_err = ""
	if ret_array["server"] == -1:
		ret_err += "Nie znaleziono podanego serwera.\n"
	if ret_array["channel"] == -1:
		ret_err += "Nie znaleziono podanego kanału.\n"
	if ret_array["user"] == -1:
		ret_err += "Nie znaleziono podanego użytkownika.\n"
	
	if len(ret_err) > 0:
		return ret_err.strip()
	else:
		return ret_array

# Prepare conditions for the database query
def prepare_conditions(time=None, server=None, channel=None, user=None, bot=False, everyone=None, deleted=None, custom_only=None, function=None):
	conditions = ""
	today = datetime.now()
	
	# Server conditions
	
	if server:
		conditions += "AND server = {} ".format(server)
	
	# Channel conditions
	
	if channel:
		conditions += "AND channel = {} ".format(channel)
	
	# Channel conditions
	
	if user:
		conditions += "AND user = {} ".format(user)
	
	# Time conditions
	
	if time == "yesterday":
		target_date = today - timedelta(days=1)
		conditions += "AND date(time, 'localtime') = '{}' ".format(target_date.strftime('%Y-%m-%d'))
	elif time == "today":
		conditions += "AND date(time, 'localtime') = '{}' ".format(today.strftime('%Y-%m-%d'))
		
	elif time != None and re.match(r"^\d+d$", time):
		target_date = today - timedelta(days=int(re.match(r"^(\d+)d$", time)[1]))
		conditions += "AND datetime(time, 'localtime') BETWEEN '{}' AND '{}' ".format(target_date.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S'))
	elif time != None and re.match(r"^\d+h$", time):
		target_date = today - timedelta(hours=int(re.match(r"^(\d+)h$", time)[1]))
		conditions += "AND datetime(time, 'localtime') BETWEEN '{}' AND '{}' ".format(target_date.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S'))
	
	elif time == "month":
		target_date = today - timedelta(days=30)
		conditions += "AND date(time, 'localtime') BETWEEN '{}' AND '{}' ".format(target_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
	elif time == "this_month":
		conditions += "AND date(time, 'localtime') BETWEEN '{}-01' AND '{}' ".format(today.strftime('%Y-%m'), today.strftime('%Y-%m-%d'))
	elif time == "last_month":
		conditions += "AND strftime('%Y-%m', time, 'localtime') = '{}' ".format((today.replace(day=1)-timedelta(days=1)).strftime('%Y-%m'))
	
	elif time != None and time.count(",") == 1:
		tmp = time.split(",")
		dates = {
			"start" : False,
			"end" : False
		}
		
		if re.match(r"^\d{4}(-\d{2})?(-\d{2})?$", tmp[0]):
			dates["start"] = tmp[0]
		if re.match(r"^\d{4}(-\d{2})?(-\d{2})?$", tmp[1]):
			dates["end"] = tmp[1]
		
		if dates["start"] and dates["end"]:
			conditions += "AND date(time, 'localtime') BETWEEN '{}' AND '{}' ".format(dates["start"], dates["end"])
		elif dates["start"]:
			conditions += "AND date(time, 'localtime') > '{}' ".format(dates["start"])
		elif dates["end"]:
			conditions += "AND date(time, 'localtime') < '{}' ".format(dates["end"])
	
	elif time != None and re.match(r"^\d{4}(-\d{2})?(-\d{2})?$", time):
		date_format = generate_date_format(time)
		conditions += "AND strftime('{}', time, 'localtime') = '{}' ".format(date_format, time)
	
	# Ignore bot entries
	if not bot:
		conditions += "AND bot = 0 "
	
	# Select @everyone mentions
	if everyone:
		conditions += "AND everyone = 1 "
	
	# Omit deleted entries
	if deleted is not None and not deleted:
		conditions += "AND deleted = 0 "
	elif deleted:
		conditions += "AND deleted = 1 "
	
	# Select only bot function invocations
	if function is not None and function:
		conditions += "AND function IS NOT NULL "
	
	# Select only custom emojis
	if custom_only is not None and custom_only:
		conditions += "AND custom = 1 "
	
	if len(conditions) == 0:
		return "WHERE 1=1"
	else:
		return "WHERE " + conditions[4:].strip()

# Generating stats

def stats_count_messages(server, time=None, channel=None, user=None, bot=True, everyone=None, deleted=False, functions=None, db=stats, cursor=stats_c):
	conditions = prepare_conditions(time, server, channel, user, bot, everyone, deleted, None, functions)
	#print("[stats_count_messages] SELECT count(*) AS result FROM messages {}".format(conditions))
	cursor.execute("SELECT count(*) AS result FROM messages {}".format(conditions))
	return cursor.fetchone()[0]

def stats_count_emojis(server, time=None, channel=None, user=None, bot=True, custom_only=None, db=stats, cursor=stats_c):
	conditions = prepare_conditions(time, server, channel, user, bot, None, None, custom_only)
	#print("[stats_count_emojis] SELECT count(*) AS result FROM emojis {}".format(conditions))
	cursor.execute("SELECT count(*) AS result FROM emojis {}".format(conditions))
	return cursor.fetchone()[0]

def stats_users(client, server, rows=5, time=None, channel=None, user=None, bot=True, everyone=None, deleted=False, functions=None, db=stats, cursor=stats_c):
	params = (rows,)
	conditions = prepare_conditions(time, server, channel, user, bot, everyone, deleted, None, functions)
	ret = ""
	
	i = 1
	#print("[stats_users] SELECT user, count(*) AS result FROM messages {} GROUP BY user ORDER BY result DESC, user ASC LIMIT 0,?".format(conditions))
	for row in cursor.execute("SELECT user, count(*) AS result FROM messages {} GROUP BY user ORDER BY result DESC, user ASC LIMIT 0,?".format(conditions), params):
		user = find(lambda m: m.id == str(row[0]), client.get_all_members())
		ret += "#{}: {} ({})\n".format(i, user.display_name if user is not None else NOT_FOUND, row[1])
		i += 1
	
	return ret.strip()

def stats_channels(client, server, rows=5, time=None, channel=None, user=None, bot=True, everyone=None, deleted=False, functions=None, db=stats, cursor=stats_c):
	params = (rows,)
	conditions = prepare_conditions(time, server, channel, user, bot, everyone, deleted, None, functions)
	ret = ""
	
	i = 1
	#print("[stats_channels] SELECT channel, count(*) AS result FROM messages {} AND channel NOT IN {} GROUP BY channel ORDER BY result DESC, channel ASC LIMIT 0,?")
	for row in cursor.execute("SELECT channel, count(*) AS result FROM messages {} AND channel NOT IN {} GROUP BY channel ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions, CHANNELS_TO_OMIT), params):
		channel = find(lambda m: m.id == str(row[0]), client.get_all_channels())
		ret += "#{}: {} ({})\n".format(i, channel.name if channel is not None else NOT_FOUND, row[1])
		i += 1
	
	return ret.strip()

def stats_functions(client, server, rows=5, time=None, channel=None, user=None, bot=True, deleted=False, db=stats, cursor=stats_c):
	params = (rows,)
	conditions = prepare_conditions(time, server, channel, user, bot, None, deleted, None, True)
	ret = ""
	
	i = 1
	#print("[stats_functions] SELECT function, count(*) AS result FROM messages {} GROUP BY function ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions))
	for row in cursor.execute("SELECT function, count(*) AS result FROM messages {} GROUP BY function ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions), params):
		ret += "#{}: {} ({})\n".format(i, row[0], row[1])
		i += 1
	
	return ret.strip()

def stats_emojis(client, server, rows=5, time=None, channel=None, user=None, bot=False, custom_only=False, db=stats, cursor=stats_c):
	params = (rows, )
	server_obj = client.get_server(server)
	conditions = prepare_conditions(time, server, channel, user, bot, None, None, custom_only)
	ret = ""
	
	if not server:
		return "Coś skopałeś z ID serwera"
	
	i = 1
	#print("[stats_emojis] SELECT emoji, sum(count) AS result FROM emojis {} GROUP BY emoji ORDER BY result DESC, emoji ASC LIMIT 0,?".format(conditions))
	for row in cursor.execute("SELECT emoji, sum(count) AS result FROM emojis {} GROUP BY emoji ORDER BY result DESC, emoji ASC LIMIT 0,?".format(conditions), params):
		ret += "#{}: {} ({})\n".format(i, row[0], row[1])
		i += 1
	
	return ret.strip()

# Generate stats

def generate_stats(client, message, channel, arguments, stat_limit=5, bot_stats=False, hide_args=False, db=stats, cursor=stats_c):
	ret = ""
	
	query_args = parse_stats_args(client, message, arguments)
	
	# Some errors were found
	if isinstance(query_args, str):
		return query_args
	
	args_display = ""
	
	if not hide_args and (query_args["time"] is not None or query_args["channel"] is not None or query_args["user"] is not None or query_args["bot"] or query_args["everyone"]):
		args_display += "\n["
		
		if query_args["server"] is not None:
			args_display += "serwer: *{}*, ".format((client.get_server(str(query_args["server"])).name if query_args["server"] != "0" else "prywatna wiadomość"))
		
		if query_args["channel"] is not None:
			args_display += "kanał: *{}*, ".format(client.get_channel(str(query_args["channel"])).name)
		
		if query_args["user"] is not None:
			args_display += "użytkownik: *{}*, ".format(find(lambda m: m.id == str(query_args["user"]), client.get_all_members()).display_name)
		
		if query_args["time"] is not None:
			args_display += "czas: *{}*, ".format(query_args["time"])
		
		if (query_args["bot"] or query_args["user"]) is not None:
			args_display += "boty: *{}*, ".format((query_args["bot"] or not not query_args["user"]))
		
		if query_args["everyone"]:
			args_display += "everyone: *{}*, ".format(query_args["everyone"])
			
		args_display = args_display[:-2] + "]"
	
	result_count = stats_count_messages(query_args["server"], time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=False, functions=bot_stats, db=db, cursor=cursor)
	
	# Message stats
	
	if result_count == 0:
		ret += "Brak wiadomości dla zadanych parametrów.{}".format(args_display)
	else:
		deleted_count = stats_count_messages(query_args["server"], time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=True, functions=bot_stats, db=db, cursor=cursor)
		ret += "Łącznie **{}** wiadomości (oraz {} usuniętych).{}".format(result_count, deleted_count, args_display)
		
		if not query_args["user"]:
			ret += ("\n\n*Najwięksi męczyciele bota:*\n\n" if bot_stats else "\n\n*Najwięksi spamerzy:*\n\n")
			
			ret += stats_users(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=False, functions=bot_stats, db=db, cursor=cursor)
		
		if not query_args["channel"] and query_args["server"] != "0":
			ret += "\n\n*Najbardziej zaspamowane kanały:*\n\n"
			
			ret += stats_channels(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=False, functions=bot_stats, db=db, cursor=cursor)
		
		if bot_stats:
			ret += "\n\n*Najczęściej używane funkcje:*\n\n"
			
			ret += stats_functions(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), deleted=False, db=db, cursor=cursor)
	
	# Emoji stats
	
	if not bot_stats and not query_args["everyone"]:
		result_count = stats_count_emojis(query_args["server"], time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), custom_only=True, db=db, cursor=cursor)
		
		if result_count == 0:
			ret += "\n\nBrak emotikon dla zadanych parametrów."
		else:
			ret += "\n\n*Najczęściej używane emoty:*\n\n"
			
			ret += stats_emojis(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), custom_only=True, db=db, cursor=cursor)
	
	return ret

# Commands

@asyncio.coroutine
def c_stats(client, message):
	stat_limit = 15 if (str(message.channel).startswith("Direct Message") or message.channel.id in ["319056762814595076", "386148571529084929"]) else 5
	bot_stats = True if "bot" in sh.get_command(message).lower() else None
	
	mmmsmsm = generate_stats(client, message, message.channel, sh.get_args(message), stat_limit, bot_stats)
	#print("Generated successfully")
	#yield from client.send_message(message.channel, "test")
	yield from client.send_message(message.channel, mmmsmsm)
	#print("Sent")

c_stats.command = r"(bot|stat)(s|ystyki)"
c_stats.desc = "hidden"


@asyncio.coroutine
def c_stattest2(client, message):
	yield from t_daily_stats(client, [message.channel])

c_stattest2.command = r"stat_test"
c_stattest2.desc = "hidden"


# Daily stats

@asyncio.coroutine
def t_daily_stats(client, channels):
	yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
	ret = "Statystyki z dnia **{}**\n".format(yesterday)
		
	for ch in channels:
		channels_new = filter(lambda m: re.search("174449535811190785", m.server.id, flags=re.I), client.get_all_channels())
		start_date = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

		# Open database
		stats_tmp = sqlite3.connect(":memory:")
		stats_tmp_c = stats_tmp.cursor()

		# Init database if necessary
		stats_tmp_c.execute(MSG_INIT_STRING)
		stats_tmp_c.execute(EMO_INIT_STRING)
		stats_tmp.commit()
		
		for cha in channels_new:
			if cha.type != discord.ChannelType.text:
				continue
			print(cha.name)
			try:
				for message in list((yield from client.logs_from(cha, limit=999999999999999, after=start_date))):
					print("t")
					insert_msg(message, db=stats_tmp, cursor=stats_tmp_c, tmp=True)
					emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
					custom_emoji_list = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
					insert_emojis_post(message, emoji_list, custom_emoji_list, db=stats_tmp, cursor=stats_tmp_c, tmp=True)
			
			except discord.Forbidden:
				continue
		print("lel")
		e = ret + generate_stats(client, None, ch, "server=politbiuro bot=t", 10, hide_args=True)
		stats_tmp.close()

		yield from client.send_message(ch, e)
		#yield from client.send_message(ch, ret + generate_stats(client, None, ch, "time=yesterday server=politbiuro bot=t", 10, hide_args=True))

t_daily_stats.channels = ["174449535811190785"]
t_daily_stats.time = "17:14"

# Weekly stats

@asyncio.coroutine
def t_weekly_stats(client, channels):
	if datetime.now().weekday() == 0:
		last_monday = (datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')
		yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
		ret = "Statystyki z zeszłego tygodnia (od **{}** do **{}**)\n".format(last_monday, yesterday)
		
		for ch in channels:
			channels = filter(lambda m: re.search(ch.id, m.server.id, flags=re.I), client.get_all_channels())
			start_date = (datetime.now()-timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)

			# Open database
			stats_tmp = sqlite3.connect(":memory:")
			stats_tmp_c = stats_tmp.cursor()

			# Init database if necessary
			stats_tmp_c.execute(MSG_INIT_STRING)
			stats_tmp_c.execute(EMO_INIT_STRING)
			stats_tmp.commit()

			for ch in channels:
				if ch.type != discord.ChannelType.text:
					continue

				try:
					for message in reversed(list((client.logs_from(ch, limit=999999999999999, after=start_date)))):
						insert_msg(message, db=stats_tmp, cursor=stats_tmp_c, tmp=True)
						emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
						custom_emoji_list = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
						insert_emojis_post(message, emoji_list, custom_emoji_list, db=stats_tmp, cursor=stats_tmp_c, tmp=True)
				
				except discord.Forbidden:
					continue
			
			e = ret + generate_stats(client, None, ch, "server=politbiuro bot=t", 10, hide_args=True)
			stats_tmp.close()

			yield from client.send_message(ch, ret + generate_stats(client, None, ch, "server=politbiuro bot=t", 15, hide_args=True))
			#yield from client.send_message(ch, ret + generate_stats(client, None, ch, "time={},{} server=politbiuro bot=t".format(last_monday, yesterday), 15, hide_args=True))

t_weekly_stats.channels = ["174449535811190785"]
t_weekly_stats.time = "00:15"


# Monthly stats

@asyncio.coroutine
def t_monthly_stats(client, channels):
	if datetime.now().strftime('%d') == "01":
		last_month = (datetime.now() - timedelta(days=1)).strftime('%Y-%m')
		ret = "Statystyki z zeszłego miesiąca (**{}**)\n".format(last_month)
		
		for ch in channels:
			channels = filter(lambda m: re.search(ch.id, m.server.id, flags=re.I), client.get_all_channels())
			start_date = (datetime.now()-timedelta(days=1)).replace(days=1, hour=0, minute=0, second=0, microsecond=0)

			# Open database
			stats_tmp = sqlite3.connect(":memory:")
			stats_tmp_c = stats_tmp.cursor()

			# Init database if necessary
			stats_tmp_c.execute(MSG_INIT_STRING)
			stats_tmp_c.execute(EMO_INIT_STRING)
			stats_tmp.commit()

			for ch in channels:
				if ch.type != discord.ChannelType.text:
					continue

				try:
					for message in reversed(list((message in client.logs_from(ch, limit=999999999999999, after=start_date)))):
						insert_msg(message, db=stats_tmp, cursor=stats_tmp_c, tmp=True)
						emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
						custom_emoji_list = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
						insert_emojis_post(message, emoji_list, custom_emoji_list, db=stats_tmp, cursor=stats_tmp_c, tmp=True)
				
				except discord.Forbidden:
					continue
			
			e = ret + generate_stats(client, None, ch, "server=politbiuro bot=t", 10, hide_args=True)
			stats_tmp.close()

			yield from client.send_message(ch, ret + generate_stats(client, None, ch, "server=politbiuro bot=t", 15, hide_args=True))
			#yield from client.send_message(ch, ret + generate_stats(client, None, ch, "time=last_month server=politbiuro bot=t", 15, hide_args=True))

t_monthly_stats.channels = ["174449535811190785"]
t_monthly_stats.time = "00:30"