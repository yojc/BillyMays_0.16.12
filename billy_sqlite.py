# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# App keys
from config import billy_key

# import logging
import random
import re
import sys
import datetime
import emoji

from imp import find_module

try:
	find_module('colorama')
	from colorama import Fore, Style, init as colorama_init
	colorama_init()
	def print_warning(text):
		print(Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL)
except ImportError:
	def print_warning(text):
		print(text)
	print("Colorama library not installed, errors won't be colorized")

# Shared functions

import billy_antiflood as af
import billy_shared as sh

# List modules to import here
# Names must start with billy_c

import billy_c_stats

# Set up logging
# import logging
# import time
# 
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='billy{}.log'.format(int(time.time())), encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Hi, Billy Mays here", command_prefix= r"^[;!\.,\/\\\\]", pm_help = True)

# Used to run timer-based function once a day
current_day = {}

def compile_command(regex):
	return client.command_prefix + regex + r"\b"

# Filling in commands/triggers list

c_functions = [] # commands
f_functions = [] # fulltext
t_functions = [] # timer-based

modules = list(set(sys.modules) & set(globals()))

for module_name in modules:
	if module_name.startswith("billy_c_"):
		i = 0
		module = sys.modules[module_name]
		
		for name, val in module.__dict__.items():
			if callable(val) and name.startswith(("c_", "f_", "t_")):
				if name.startswith("t_"):
					if hasattr(val, "time") and not re.match(r"([0-9]|[0-1][0-9]|2[0-3])\:[0-5][0-9]", getattr(val, "time")):
						print("Invalid specified time: " + name)
						continue
					elif not hasattr(val, "channels"):
						print("No channels specified: " + name)
						continue
					else:
						# Timer functions functions
						sh.debug("Imported timer: " + name)
						t_functions.append(val)
						i += 1
				
				elif not hasattr(val, "command"):
					# Omit functions without specified .command
					print("Missing command regex: " + name)
					continue
				
				elif name.startswith("f_") and not hasattr(val, "prob"):
					# Omit fulltext without specified .prob
					print("Missing fulltext probability: " + name)
					continue
				
				elif name.startswith("c_"):
					# Called functions
					sh.debug("Imported command: " + name)
					c_functions.append(val)
					i += 1
				
				elif name.startswith("f_"):
					# Fulltext search
					sh.debug("Imported fulltext: " + name)
					f_functions.append(val)
					i += 1
			
		print("Loaded " + str(i) + " functions from module " + module_name)
	else:
		sh.debug("Probably not a module: " + module_name)

# Start timer tasks

for e in t_functions:
	def f(fun):
		global client
		global current_day
		yield from client.wait_until_ready()
		
		if hasattr(fun, "time"):
			t = list(map(int, getattr(fun, "time").split(":")))
		else:
			t = False
		
		channels = []
		tmp = getattr(fun, "channels")
		for e in tmp:
			channels.append(discord.Object(id=e))
		
		interval = getattr(fun, "interval", 30)
		
		while not client.is_closed:
			now = datetime.datetime.now()
			
			if (not fun.__name__ in current_day or current_day[fun.__name__] != now.day) and (not t or (t[0] == now.hour and t[1] == now.minute)):
				current_day[fun.__name__] = now.day
				yield from fun(client, channels)
			
			yield from asyncio.sleep(interval)
	
	client.loop.create_task(f(e))

# Parse message and execute functions

@asyncio.coroutine
def parse_message(message, edited=False):
	if not edited:
		billy_c_stats.insert_msg(message)
	
	# Track used emojis
	
	emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
	custom_emoji_list = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
	billy_c_stats.insert_emojis_post(message, emoji_list, custom_emoji_list, edited)
	
	# ignore bot messages
	
	if message.author == client.user:
		return
	
	perm = af.check_channel_whitelist(client, message)
	
	# channel blacklisted
	
	if perm["disallow"]:
		return
	
	# strip quotes
	content = sh.rm_leading_quotes(message)
	
	
	if not edited:
		# fulltext search
		for f in f_functions:
			c = getattr(f, "command", False)
			p = getattr(f, "prob", False)
			
			if c and p and re.search(c, content, re.IGNORECASE) and (p >= 1.0 or (perm["fulltext"] and random.random() < p)):
				sh.debug("Triggered " + f.__name__ + "...")
				try:
					yield from f(client, message)
				except Exception:
					print_warning("An error occured in " + f.__name__ + "!!! (" + content + ")")
					raise
					
	# commands
	
	if re.match(client.command_prefix, content):
		sh.debug("This seems to be a command: " + sh.get_command(message))
		
		# check antiflood
		
		#if perm["flood"] and ((yield from af.check_flood_channel(client, message)) or (yield from af.check_flood(client, message))):
		#	sh.debug("Anti-flood kicked in yo")
		#	return
		
		# help
		
		# not needed here
		
		#else:
		# iterate over functions
		for f in c_functions:
			c = getattr(f, "command", False)
			r = re.match(compile_command(c), content, re.IGNORECASE)
			if c and r:
				sh.debug("Executing " + f.__name__ + "...")
				yield from client.send_typing(message.channel)
				try:
					yield from f(client, message)
					billy_c_stats.update_msg_function(message, f.__name__)
				except Exception:
					yield from client.send_message(message.channel, "Oho, chyba jakiś błąd w kodzie. <@307949259658100736> to kiedyś naprawi, jak się skończy bawić pociągami.")
					print_warning("An error occured in " + f.__name__ + "!!! (" + content + ")")
					#CZEMU TY CHUJU NIE DZIALASZ
					#logging.exception("An error occured in " + f.__name__ + "!!! (" + content + ")")
					raise
					continue
				break
		
		

# Sort functions alphabetically (for .help)
c_functions.sort(key=lambda x: x.__name__)
print("--------")

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
	print('--------')
	
	#yield from billy_c_sopel_remind.setup(client)


# Execute on every reaction

@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
	# track used emojis
	billy_c_stats.insert_emojis_reaction(reaction.message, user, reaction.emoji, reaction.custom_emoji)
	
	if reaction.me:
		return
	
	#if random.random() < 0.001:
	#	yield from asyncio.sleep(4)
	#	yield from client.add_reaction(reaction.message, reaction.emoji)

@client.event
@asyncio.coroutine
def on_reaction_remove(reaction, user):
	# track used emojis
	billy_c_stats.remove_reaction(reaction.message, user, reaction.emoji, reaction.custom_emoji)


# Execute on every msg edit

@client.event
@asyncio.coroutine
def on_message_edit(before, after):
	if before.content == after.content:
		return
	
	yield from parse_message(after, True)

# Execute on every msg

@client.event
@asyncio.coroutine
def on_message(message):
	yield from parse_message(message)

# Handle reponse deletion

@client.event
@asyncio.coroutine
def on_message_delete(message):
	billy_c_stats.update_msg_deletion(message)
	
	content = sh.rm_leading_quotes(message)
	
	if message.author == client.user or not message.server or not re.match(client.command_prefix, content):
		return
	
	sh.debug("User message deleted: " + message.content, message)
	
	for log in reversed(list((yield from client.logs_from(message.channel, limit=50, after=message)))):
		if log.author != client.user or not log.content.startswith("<@!" + message.author.id + ">:"):
			continue
		
		sh.debug("Found a message to delete: " + log.content, message)
		
		yield from client.delete_message(log)
		return
	
	sh.debug("No matching bot response found")

# Bot ID
client.run(billy_key)