# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

import random
import emoji
import re
#from time import sleep

from config import kathai_key

client = Bot(description="xD", command_prefix= "dupa", pm_help = True)
game_synced = None

# Games to play

game_list = ["Borderlands", "Borderlands 2", "Borderlands 3", "Borderlands: the Pre-Sequel!", "Dragon Age: Origins", "Tales from the Breslau", "Genital Jousting", "Team Fortress 2", "Crusaders of the Lost Idols", "Mining Industry Simulator", "Plush", "Chamsko: The Rift", "Overwatch", "Tom Hardy: The Game", "Silesia Tycoon", "PAC-MAN", "Call of Kopalnioki"]


# Action probability

prob_reply = 0.025
prob_react = 0.05
prob_react_as_reply = 0.3
prob_game = 0.01


# Repeat emojis from messages/reactions?

repeat_emoji = False
repeat_reaction = False


# Channel whitelist

channels = ["politbiuro", "luzna_jazda", "spotkania_politbiura"]


# Owners

master = "307949259658100736"
owners = []

# Possible replies go here

def f_iksde(message):
	iter = 1
	
	if random.random() < 0.5:
		reply = "X"
	else:
		reply = "x"
	
	if random.random() < 0.3:
	
		if random.random() < 0.6:
			iter = random.randint(2, 4)
		else:
			iter = random.randint(3, 6)
	
	for _ in range(iter):
		reply += "D"
	
	return reply

f_iksde.prob = 0.59


def f_chamsko(message):
	if random.random() < 0.7:
		reply = "chamsko"
		
		if random.random() < 0.3:
			if random.random() < 0.5:
				reply += "!"
			else:
				reply += " XD"
	elif random.random() < 0.5:
		reply = random.choice(["najchamściej", "NAJCHAMŚCIEJ"])
	else:
		reply = "borze, jak chamsko"
	
	return reply

f_chamsko.prob = 0.14


def f_pac(message):
	reply = random.choice(["\*pac*", "\*PAC*", "\*PACPACPAC*"])
	
	return reply

f_pac.prob = 0.05


def f_pff(message):
	reply = "p"
	for _ in range(random.randint(2, 6)):
		reply += "f"
	
	return reply

f_pff.prob = 0.03


def f_nie(message):
	reply = "NIE"
	if random.random() < 0.5:
		reply += "!"
	
	if random.random() < 0.1:
		reply = "borze, " + reply
	
	return reply

f_nie.prob = 0.04


def f_czo(message):
	if random.random() < 0.6:
		reply = "czo"
		if random.random() < 0.3:
			reply += " xD"
	else:
		reply = "CZO"
		if random.random() < 0.3:
			if random.random() < 0.5:
				reply += " XD"
			else:
				reply += " XDDD"
	
	return reply

f_czo.prob = 0.04


def f_trzy(message):
	reply = random.choice([":3", ":D", ":/", "\U00002764", "\U0001F922", "\U0001F44D", "\U00002764", "<:mhhhmm:256873687871913984>", "<:podbiel:326424787121602560>", "<:brwinow:349219149614022666>", "<:angery:325368048640983052>", "<:paweeel:397807577699975181>"])
	
	return reply

f_trzy.prob = 0.03


def f_typalo(message):
	nick = message.author.name
	mapping = { 
		"st3fan0" : "Stefan",
		"Giant Dad" : "Xardas",
		"Bert" : "b3rt",
		"Matt J." : "Black Shadow",
		"Xy" : "Xysiu",
		"Infel" : "Dracia",
		"SirAleksanderHeim" : "Artius",
		"Shakecaine" : "Shaker",
		"POLIPOLIK" : "POLIP",
		"Billy Mays" : "Billy",
		"wies.niak" : "wiesiu"
	}
	
	if nick in mapping:
		nick = nick.replace(nick, mapping[nick])
	
	reply = random.choice([
		"{}, {}y pało{}".format(nick, random.choice(["T", "t"]), random.choice(["", "!"])),
		"{}{}, cho{} na {}!".format(random.choice(["", "ej "]), nick, random.choice(["", "dź"]), random.choice(["Bordery", "Overwatcha", "TSa"]))
	])
	
	return reply

f_typalo.prob = 0.02


def f_whew(message):
	reply = random.choice(["whew", "WHEW", "w h e w", "W H E W"])
	
	return reply

f_whew.prob = 0.03


def f_borze(message):
	reply = random.choice(["borze", "BORZE"])
	
	return reply

f_borze.prob = 0.03


# Helper functions

def is_private_msg(message):
	return str(message.channel).startswith("Direct Message")

def is_mentioned(message, user=None):
	if user:
		return (message.server and message.server.get_member_named(user) in message.mentions)
	else:
		return (message.server and (message.server.get_member_named("Kath#8040") in message.mentions or message.server.me in message.mentions))

def choose_reply(message):
	prob_weight = 1.0/prob_total
	prob_left = 1.0
	
	for f in f_list:
		prob_current = (1/prob_left) * prob_weight * f.prob
		#print(f.__name__ + " " + str(f.prob) + " (" + str(prob_current) + ")")
		if random.random() < prob_current:
			#print("Fired")
			return f(message)
		else:
			prob_left -= (prob_weight * f.prob)

def list_functions():
	global f_list
	global prob_total
	
	f_list = []
	prob_total = 0
	
	for name, val in globals().items():
		if callable(val) and name.startswith("f_"):
			if not hasattr(val, "prob"):
				print("Missing command probability: " + name)
				continue
			else:
				f_list.append(val)
				prob_total += getattr(val, "prob")
				print("Activated function " + name + " with activation probability " + str(getattr(val, "prob")))
	
	print("Found " + str(len(f_list)) + " functions total, summarised probability: " + str(prob_total))
	print('--------')

@asyncio.coroutine
def trigger_reactions(message):
	slept = False
	
	r_list = [
		{"regex" : r'pizz.*(ananas|hawa)|(ananas|hawa).*pizz', "reaction" : ["\U0001F355", "\U0001F34D"], "extra_check" : False, "probability" : 1, "might_reply" : False},
		{"regex" : r'vkPCjJM.jpg', "reaction" : [random.choice(["\U0001F922", "\U0001F645", "\U0001F6AB"])], "extra_check" : False, "probability" : 1, "might_reply" : True},
		{"regex" : r'(3tsmuxa|We8ms5m).jpg', "reaction" : [random.choice(["\U0001F6AC", "\U0001F6AD"])], "extra_check" : False, "probability" : 1, "might_reply" : False},
		{"regex" : r'nerv', "reaction" : ["\U0001F354"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'kat(h|ai|aj|owic)', "reaction" : [random.choice(["\U0001F44D", "\U00002764"])], "extra_check" : is_mentioned(message), "probability" : prob_react, "might_reply" : True},
		{"regex" : r'(?<!m)artius', "reaction" : ["\U0001F942"], "extra_check" : is_mentioned(message, "SirAleksanderHeim#6341"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\brysi', "reaction" : [random.choice(["\U0001F431", "\U0001F408"])], "extra_check" : is_mentioned(message, "Rysia#1973"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'rankin', "reaction" : ["blini:256876147810369556"], "extra_check" : is_mentioned(message, "rane#2794"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\bteb', "reaction" : [random.choice(["\U0001F436", "\U0001F415"])], "extra_check" : is_mentioned(message, "Teb#2096"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\bkice|kick', "reaction" : [random.choice(["🏳️‍🌈", "\U0001F308", "\U0001F407", "\U0001F430"])], "extra_check" : is_mentioned(message, "kiceg#1555"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'pewker|palker|pałker', "reaction" : ["\U0001F4A9"], "extra_check" : is_mentioned(message, "Pewker#3465"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'papie(z|ż)|jp2|wojty(l|ł)a|krem(o|ó)wk|watykan|vatican', "reaction" : ["🇻🇦"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\bbryl|brwi', "reaction" : ["brwinow:349219149614022666"], "extra_check" : is_mentioned(message, "brylant#7668"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'podbiel', "reaction" : ["podbiel:326424787121602560"], "extra_check" : is_mentioned(message, "podbiel#4486"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'wąż|wonsz|snake|snek', "reaction" : ["\U0001F40D"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'p_?aul', "reaction" : [random.choice(["\U0001F4A3", "paweeel:397807577699975181"])], "extra_check" : is_mentioned(message, "P_aul#1696"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'hrabul', "reaction" : [random.choice(["\U0001F4B2", "\U0001F4B5"])], "extra_check" : is_mentioned(message, "hrabula#4726"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'@(everyone|here)', "reaction" : ["angery:325368048640983052"], "extra_check" : message.mention_everyone, "probability" : prob_react, "might_reply" : True},
		{"regex" : r'\borg(u|iel|ieł)', "reaction" : [random.choice(["coolczesc:325367097125502989", "🇮🇱"])], "extra_check" : is_mentioned(message, "orgiele#8308"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\bfel', "reaction" : ["\U0001F388"], "extra_check" : is_mentioned(message, "Fel#6728"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'xd|iksde', "reaction" : random.choice([["pacaj:424902606637498391"], ["\U0001F1FD", "\U0001F1E9"]]), "extra_check" : False, "probability" : prob_react/3, "might_reply" : False},
		{"regex" : r'vod(a|ę|zi|e)|tarkin', "reaction" : ["cyka:369039064533303318"], "extra_check" : is_mentioned(message, "Tarkin#6128"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'czekolad|chocolat', "reaction" : ["\U0001F36B"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\bm[mh]{2,}|dup(a|ą|ie|y)|penis|beni(s|z)|kutas|cycek|cyck|piersi|tyłek|tylek|dojce|loda', "reaction" : ["mhhhmm:256873687871913984"], "extra_check" : False, "probability" : prob_react, "might_reply" : True},
		{"regex" : r'(gofer|gofr)', "reaction" : ["\U0001F984"], "extra_check" : is_mentioned(message, "Gofer#9218"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'martius', "reaction" : ["\U0001F426"], "extra_check" : is_mentioned(message, "Knight Martius#1640"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'\bdzik', "reaction" : ["\U0001F417"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'draci', "reaction" : ["\U0001F409"], "extra_check" : is_mentioned(message, "Dracia#6218"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'(\bhm+\b|mo(z|ż).*|czy.*\?)', "reaction" : [random.choice(["tonk:293675913290317825", "hyperthink:383238503913357313"])], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'brawo|brawa|poleca', "reaction" : [random.choice(["gato:339849333530689537", "znak:391940544458391565"])], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'darmo|janusz|polac|polak|promoc|tani', "reaction" : ["janusz:398923553736622107"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'pewien|pewn', "reaction" : ["jestespewien:328913959342178304"], "extra_check" : False, "probability" : prob_react, "might_reply" : False},
		{"regex" : r'xardas|czardas|ściaz|sciaz', "reaction" : [random.choice(["sadpepe:256873871037300736", "sadface:256877855378636810"])], "extra_check" : is_mentioned(message, "Giant Dad#3849"), "probability" : prob_react, "might_reply" : False},
		{"regex" : r'nargog', "reaction" : [random.choice(["smaglor:328947669676457984", "komarcz:328946510274232330"])], "extra_check" : is_mentioned(message, "Giant Dad#3849"), "probability" : prob_react, "might_reply" : False}
	]
	
	for r in r_list:
		if (re.search(r["regex"], message.content, re.IGNORECASE) or r["extra_check"]) and (is_private_msg(message) or random.random() < r["probability"]):
			if not slept:
				yield from asyncio.sleep(1)
				slept = True
			
			if r["might_reply"] and (is_private_msg(message) or str(message.channel) in channels) and random.random() < prob_react_as_reply:
				emoji = "<:{}>".format(r["reaction"][0]) if ":" in r["reaction"][0] else r["reaction"][0]
				yield from client.send_message(message.channel, emoji)
			else:
				for e in r["reaction"]:
					try:
						yield from client.add_reaction(message, e)
						#print("Success: {}, {}, {}".format(message.channel, message.author, e.encode('raw_unicode_escape')))
					except Exception:
						print("Failure: {}, {}, {}, {}".format(message.channel, message.author, e.encode('raw_unicode_escape'), r["regex"]))
						raise

'''
# Check user message for commands
@asyncio.coroutine
def parse_commands(message):
	global master
	global owners

	if message.author.id != master or message.author.id not in owners:
		return True

	elif message.content.startswith(".send"):
		args = message.content.split(None, 2)
		client.get_channel(args[1]).send(args[2])
		return False

	else:
		return True
'''


# Execute on every reaction
@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
	if repeat_reaction:
		if reaction.me:
			return
		
		#if is_private_msg(reaction.message) or (str(reaction.message.channel) in channels and random.random() < prob_reply):
		#	yield from client.send_message(reaction.message.channel, choose_reply())
		
		if is_private_msg(reaction.message) or random.random() < prob_react:
			yield from asyncio.sleep(4)
			yield from client.add_reaction(reaction.message, reaction.emoji)


# Execute on every msg
@client.event
@asyncio.coroutine
def on_message(message):
	global game_synced
	
	if message.author == client.user:
		return
	
	# Check for commands

	global master
	global owners

	if message.author.id == master or message.author.id in owners:

		if message.content.startswith(".send"):
			args = message.content.split(None, 2)
			channel = client.get_channel(args[1])
			msg = args[2]
			yield from client.send_message(channel, msg)
			return

		elif message.content.startswith(".react"):
			args = message.content.split(None, 3)
			channel = client.get_channel(args[1])
			msg = yield from client.get_message(channel, args[2])
			react = args[3]
			yield from client.add_reaction(msg, react)
			return
	
	# Sync game
	
	if message.server and message.server.get_member_named("Kath#8040") and message.server.get_member_named("Kath#8040").game and game_synced != message.server.get_member_named("Kath#8040").game:
	#and re.search(r"borderlands", message.server.get_member_named("Kath#8040").game.name, re.IGNORECASE):
		game_synced = message.server.get_member_named("Kath#8040").game
		yield from client.change_presence(game=message.server.get_member_named("Kath#8040").game)
	elif not is_private_msg(message) and random.random() < prob_game:
		game_synced = None
		yield from client.change_presence(game=discord.Game(name=random.choice(game_list)))
	
	# Add a reaction
	if (not message.author.bot and not re.match(r"^[!\.,\/\\\\]", message.content.strip())):
		yield from trigger_reactions(message)
	
	# Repeat emoji from post
	if repeat_emoji:
		emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
		custom_emoji_list = re.findall(r"(?<=:)\S+?:\d+", message.clean_content, re.IGNORECASE) or []
		custom_emoji_list_raw = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
		if not message.author.bot and len(emoji_list+custom_emoji_list) > 0 and (is_private_msg(message) or random.random() < prob_react):
			if (is_private_msg(message) or str(message.channel) in channels) and random.random() < prob_react_as_reply:
				yield from client.send_typing(message.channel)
				yield from asyncio.sleep(1)
				yield from client.send_message(message.channel, random.choice(emoji_list+custom_emoji_list_raw))
				return
			else:
				yield from asyncio.sleep(1)
				yield from client.add_reaction(message, random.choice(emoji_list+custom_emoji_list))
	
	# Lie
	
	if str(message.channel) == "spotkania_politbiura" and (message.mention_everyone or is_mentioned(message)) and random.random() < 0.2:
		yield from client.send_message(message.channel, random.choice(["niestety, tym razem nie przyjadę :("]))
		return
	
	# Check if allowed to reply in this channel
	
	if not is_private_msg(message) and str(message.channel) not in channels:
		return
	
	# Check probability
	
	if not is_private_msg(message) and random.random() > prob_reply:
		return
	
	iksde = choose_reply(message)
	yield from client.send_typing(message.channel)
	yield from asyncio.sleep(1)
	yield from client.send_message(message.channel, iksde)
	
	if iksde.lower().startswith("x") and random.random() < 0.04:
		yield from client.send_typing(message.channel)
		yield from asyncio.sleep(1)
		yield from client.send_message(message.channel, "{} {}".format(random.choice(["TAK", "tak"]), random.choice(["", "\U00002764"])))


# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
@asyncio.coroutine
def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	
	yield from client.change_presence(game=discord.Game(name=random.choice(game_list)))
	
	# Join AFK
	try:
		yield from client.join_voice_channel(client.get_channel("174536838780944384"))
	except: 
		pass
	


# Loop through functions

list_functions()


# Start
client.run(kathai_key)