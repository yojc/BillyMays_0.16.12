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

game_list = ["Borderlands", "Borderlands 2", "Borderlands 3", "Borderlands: the Pre-Sequel!", "Dragon Age: Origins", "Tales from the Borderlands", "Genital Jousting", "Team Fortress 2", "Crusaders of the Lost Idols", "Mining Industry Simulator", "Plush", "Chamsko: The Rift", "Overwatch"]


# Action probability

prob_reply = 0.025
prob_react = 0.05
prob_game = 0.01


# Channel whitelist

channels = ["politbiuro", "luzna_jazda", "spotkania_politbiura"]


# Possible replies go here

def f_iksde():
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

f_iksde.prob = 0.6


def f_chamsko():
	reply = "chamsko"
	
	if random.random() < 0.3:
		if random.random() < 0.5:
			reply += "!"
		else:
			reply += " XD"
	
	return reply

f_chamsko.prob = 0.14


def f_pac():
	return "\*pac*"

f_pac.prob = 0.06


def f_pff():
	reply = "p"
	for _ in range(random.randint(2, 6)):
		reply += "f"
	
	return reply

f_pff.prob = 0.06


def f_nie():
	reply = "NIE"
	if random.random() < 0.5:
		reply += "!"
	
	return reply

f_nie.prob = 0.05


def f_czo():
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

f_czo.prob = 0.06


def f_trzy():
	reply = random.choice([":3", ":D"])
	
	return reply

f_trzy.prob = 0.03


# Helper functions

def is_private_msg(message):
	return str(message.channel).startswith("Direct Message")

def is_mentioned(message, user=None):
	if user:
		return (message.server and message.server.get_member_named(user) in message.mentions)
	else:
		return (message.server and (message.server.get_member_named("Kath#8040") in message.mentions or message.server.me in message.mentions))

def choose_reply():
	prob_weight = 1.0/prob_total
	prob_left = 1.0
	
	for f in f_list:
		prob_current = (1/prob_left) * prob_weight * f.prob
		#print(f.__name__ + " " + str(f.prob) + " (" + str(prob_current) + ")")
		if random.random() < prob_current:
			#print("Fired")
			return f()
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
		{"regex" : r'pizz.*(ananas|hawa)|(ananas|hawa).*pizz', "reaction" : ["\U0001F355", "\U0001F34D"], "extra_check" : False, "probability" : 1},
		{"regex" : r'vkPCjJM.jpg', "reaction" : [random.choice(["\U0001F922", "\U0001F645", "\U0001F6AB"])], "extra_check" : False, "probability" : 1},
		{"regex" : r'nerv', "reaction" : ["\U0001F354"], "extra_check" : False, "probability" : prob_react},
		{"regex" : r'kat(h|ai|aj|owic)', "reaction" : [random.choice(["\U0001F44D", "\U00002764"])], "extra_check" : is_mentioned(message), "probability" : prob_react},
		{"regex" : r'artius', "reaction" : ["\U0001F942"], "extra_check" : is_mentioned(message, "SirAleksanderHeim#6341"), "probability" : prob_react},
		{"regex" : r'rysi', "reaction" : [random.choice(["\U0001F431", "\U0001F408"])], "extra_check" : is_mentioned(message, "Rysia#1973"), "probability" : prob_react},
		{"regex" : r'rankin', "reaction" : ["blini:256876147810369556"], "extra_check" : is_mentioned(message, "rane#2794"), "probability" : prob_react},
		{"regex" : r'teb', "reaction" : [random.choice(["\U0001F436", "\U0001F415"])], "extra_check" : is_mentioned(message, "Teb#2096"), "probability" : prob_react},
		{"regex" : r'kice|kick', "reaction" : [random.choice(["🏳️‍🌈", "\U0001F308", "\U0001F407", "\U0001F430"])], "extra_check" : is_mentioned(message, "kiceg#1555"), "probability" : prob_react},
		{"regex" : r'pewker|palker|pałker', "reaction" : ["\U0001F4A9"], "extra_check" : is_mentioned(message, "Pewker#3465"), "probability" : prob_react},
		{"regex" : r'papie(z|ż)|jp2|wojty(l|ł)a|krem(o|ó)wk|watykan|vatican', "reaction" : ["🇻🇦"], "extra_check" : False, "probability" : prob_react},
		{"regex" : r'bryl|brwi', "reaction" : ["brwinow:349219149614022666"], "extra_check" : is_mentioned(message, "brylant#7668"), "probability" : prob_react},
		{"regex" : r'podbiel', "reaction" : ["podbiel:326424787121602560"], "extra_check" : is_mentioned(message, "podbiel#4486"), "probability" : prob_react},
		{"regex" : r'wąż|wonsz|snake|snek', "reaction" : ["\U0001F40D"], "extra_check" : False, "probability" : prob_react},
		{"regex" : r'p_?aul', "reaction" : ["\U0001F4A3"], "extra_check" : is_mentioned(message, "P_aul#1696"), "probability" : prob_react},
		{"regex" : r'hrabul', "reaction" : [random.choice(["\U0001F4B2", "\U0001F4B5"])], "extra_check" : is_mentioned(message, "hrabula#4726"), "probability" : prob_react},
		{"regex" : r'@(everyone|here)', "reaction" : ["angery:325368048640983052"], "extra_check" : message.mention_everyone, "probability" : prob_react},
		{"regex" : r'org(u|iel|ieł)', "reaction" : ["coolczesc:325367097125502989"], "extra_check" : is_mentioned(message, "orgiele#8308"), "probability" : prob_react},
		{"regex" : r'fel', "reaction" : ["\U0001F388"], "extra_check" : is_mentioned(message, "Fel#6728"), "probability" : prob_react},
		{"regex" : r'xd', "reaction" : ["\U0001F1FD", "\U0001F1E9"], "extra_check" : False, "probability" : prob_react},
		{"regex" : r'vod(a|ę|zi|e)|tarkin', "reaction" : ["cyka:369039064533303318"], "extra_check" : is_mentioned(message, "Tarkin#6128"), "probability" : prob_react},
		{"regex" : r'czekolad|chocolat', "reaction" : ["\U0001F36B"], "extra_check" : False, "probability" : prob_react},
		{"regex" : r'm[mh]{1,}m|dup(a|ą|ie|y)|penis|kutas|cycek|cyck|piersi|tyłek|tylek', "reaction" : ["mhhhmm:256873687871913984"], "extra_check" : False, "probability" : prob_react},
		{"regex" : r'dzik', "reaction" : ["\U0001F417"], "extra_check" : False, "probability" : prob_react}
	]
	
	for r in r_list:
		if (re.search(r["regex"], message.content, re.IGNORECASE) or r["extra_check"]) and (is_private_msg(message) or random.random() < r["probability"]):
			if not slept:
				yield from asyncio.sleep(1)
				slept = True
			
			for e in r["reaction"]:
				try:
					yield from client.add_reaction(message, e)
					#print("Success: {}, {}, {}".format(message.channel, message.author, e.encode('raw_unicode_escape')))
				except Exception:
					print("Failure: {}, {}, {}, {}".format(message.channel, message.author, e.encode('raw_unicode_escape'), r["regex"]))
					raise
					continue



# Execute on every reaction
@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
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
	
	# Sync game
	
	if message.server and message.server.get_member_named("Kath#8040") and message.server.get_member_named("Kath#8040").game and game_synced != message.server.get_member_named("Kath#8040").game:
	#and re.search(r"borderlands", message.server.get_member_named("Kath#8040").game.name, re.IGNORECASE):
		game_synced = message.server.get_member_named("Kath#8040").game;
		yield from client.change_presence(game=message.server.get_member_named("Kath#8040").game)
	elif not is_private_msg(message) and random.random() < prob_game:
		game_synced = None;
		yield from client.change_presence(game=discord.Game(name=random.choice(game_list)))
	
	# Add a reaction
	if (not message.author.bot and not re.match(r"^[!\.,\/\\\\]", message.content.strip())):
		yield from trigger_reactions(message)
	
	# Repeat emoji from post
	emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
	custom_emoji_list = re.findall(r"(?<=:)\S+?:\d+", message.clean_content, re.IGNORECASE) or []
	custom_emoji_list_raw = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
	if len(emoji_list+custom_emoji_list) > 0 and (is_private_msg(message) or random.random() < prob_react):
		if (is_private_msg(message) or str(message.channel) in channels) and random.random() < 0.4:
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
	
	iksde = choose_reply()
	yield from client.send_typing(message.channel)
	yield from asyncio.sleep(1)
	yield from client.send_message(message.channel, iksde)
	
	if iksde.lower().startswith("x") and random.random() < 0.05:
		yield from client.send_typing(message.channel)
		yield from asyncio.sleep(1)
		if random.random() < 0.5:
			yield from client.send_message(message.channel, "tak")
		else:
			yield from client.send_message(message.channel, "TAK")


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
	vc = yield from client.join_voice_channel(client.get_channel("174536838780944384"))


# Loop through functions

list_functions()


# Start
client.run(kathai_key)