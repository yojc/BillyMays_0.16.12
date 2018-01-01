# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

import random
import re
from time import sleep

client = Bot(description="xD", command_prefix= "dupa", pm_help = True)

# Games to play

game_list = ["Borderlands", "Borderlands 2", "Borderlands 3", "Borderlands: the Pre-Sequel!", "Dragon Age: Origins", "Tales from the Borderlands", "Genital Jousting", "Team Fortress 2", "Crusaders of the Lost Idols", "Mining Industry Simulator", "Plush", "Chamsko: The Rift"]


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

f_chamsko.prob = 0.15


def f_pac():
	return "\*pac*"

f_pac.prob = 0.08


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


# Helper functions

def is_private_msg(message):
	return str(message.channel).startswith("Direct Message")

def is_mentioned(message, user=None):
	if user:
		return (message.server and message.server.get_member_named(user) in message.mentions)
	else:
		return (message.server and (message.server.get_member_named("Kath#8040") in message.mentions or message.server.get_member_named("KatajNapsika#5915") in message.mentions))

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


# Execute on every reaction
@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
	if reaction.me:
		return
	
	#if is_private_msg(reaction.message) or (str(reaction.message.channel) in channels and random.random() < prob_reply):
	#	yield from client.send_message(reaction.message.channel, choose_reply())
	
	if is_private_msg(reaction.message) or random.random() < prob_react:
		sleep(4)
		yield from client.add_reaction(reaction.message, reaction.emoji)


# Execute on every msg
@client.event
@asyncio.coroutine
def on_message(message):
	if message.author == client.user:
		return
	
	# Change the game
	if random.random() < prob_game:
		yield from client.change_presence(game=discord.Game(name=random.choice(game_list)))
	
	# Add a reaction
	if re.match(r'pizz.*(ananas|hawaj)|(ananas|hawaj).*pizz', message.content, re.IGNORECASE):
		sleep(1)
		yield from client.add_reaction(message, "\U0001F355")
		yield from client.add_reaction(message, "\U0001F34D")
		
	if re.match(r'vkPCjJM.jpg', message.content, re.IGNORECASE):
		sleep(1)
		yield from client.add_reaction(message, "\U0001F922")
	
	if (re.match(r'kat(h|ai|aj)', message.content, re.IGNORECASE) or is_mentioned(message)) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, "\U0001F44D")
		
	if (re.match(r'nerv', message.content, re.IGNORECASE) or is_mentioned(message, "nerv0#5242")) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, "\U0001F354")
		
	if (re.match(r'artius', message.content, re.IGNORECASE) or is_mentioned(message, "SirAleksanderHeim#6341")) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, "\U0001F942")
		
	if (re.match(r'rysi|rankin', message.content, re.IGNORECASE) or is_mentioned(message, "Rysia#1973") or is_mentioned(message, "rane#2794")) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, random.choice(["\U0001F431", "\U0001F408"]))
		
	if (re.match(r'pewker|palker|pałker', message.content, re.IGNORECASE) or is_mentioned(message, "Pewker#3465")) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, "\U0001F4A9")
		
	if re.match(r'papiez|papież|jp2|wojtyła|wojtyla|kremowk|kremówk|watykan|vatican', message.content, re.IGNORECASE) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, "🇻🇦")
		
	if (re.match(r'bryl', message.content, re.IGNORECASE) or is_mentioned(message, "brylant#7668")) and (is_private_msg(message) or random.random() < prob_react):
		sleep(1)
		yield from client.add_reaction(message, "brwinow:349219149614022666")
	
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
	sleep(1)
	yield from client.send_message(message.channel, iksde)
	
	if iksde.lower().startswith("x") and random.random() < 0.05:
		yield from client.send_typing(message.channel)
		sleep(1)
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
client.run('token')
