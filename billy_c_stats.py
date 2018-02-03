import asyncio
import pickle
import sqlite3

import billy_shared as sh

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
	everyone INTEGER,
	bot_replies TEXT,
	function TEXT
)''')
stats.commit()


def insert_msg(msg):
	data = (msg.id, msg.server.id if msg.server is not None else 0, msg.channel.id if msg.channel is not None else None, msg.author.id, msg.timestamp, msg.mention_everyone, "", None)
	
	stats_c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
	stats.commit()
	
	sh.debug("Inserted message {} into the stat database".format(msg.id))

def update_msg_function(msg, funct):
	data = (funct, msg.id)
	
	stats_c.execute("UPDATE messages SET function = ? WHERE message = ?", data)
	stats.commit()
	
	sh.debug("Updated message function: {}".format(funct))


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