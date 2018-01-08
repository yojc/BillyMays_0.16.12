# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# App keys
from config import billy_key

# Import logging
import random
import re
import sys

# Shared functions

import billy_antiflood as af
import billy_shared as sh

# List modules to import here
# Names must start with billy_c

import billy_c_yojc
import billy_c_web
import billy_c_translate
import billy_c_rhymes

# Error log location
#logging.basicConfig(filename="billy_err.log", level=logging.DEBUG)

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Hi, Billy Mays here", command_prefix= r"^[!\.,\/\\\\]", pm_help = True)

def compile_command(regex):
	return client.command_prefix + regex + r"\b"

# Filling in commands/triggers list

c_functions = [] # commands
f_functions = [] # fulltext

modules = list(set(sys.modules) & set(globals()))

for module_name in modules:
	if module_name.startswith("billy_c_"):
		i = 0
		module = sys.modules[module_name]
		
		for name, val in module.__dict__.items():
			if callable(val) and name.startswith(("c_", "f_")):
				if not hasattr(val, "command"):
					# Omit functions without specified .command
					print("Missing command regex: " + name)
					continue
				elif name.startswith("f_") and not hasattr(val, "prob"):
					# Omit fulltext without specified .prob
					print("Missing fulltext probability: " + name)
					continue
				else:
					if name.startswith("c_"):
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


# Execute on every reaction
@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
	if reaction.me:
		return
	
	if random.random() < 0.25:
		sleep(4)
		yield from client.add_reaction(reaction.message, reaction.emoji)


# Execute on every msg
@client.event
@asyncio.coroutine
def on_message(message):
	#ignore bot messages
	
	if message.author == client.user:
		return
	
	# Sync game
	
	#if message.server and message.server.get_member_named("yojc#2359") and message.server.get_member_named("yojc#2359").game and re.search(r"borderlands", message.server.get_member_named("yojc#2359").game.name, re.IGNORECASE):
	#	yield from client.change_presence(game=message.server.get_member_named("yojc#2359").game)
	#else:
	#	yield from client.change_presence(game=None)
	
	perm = af.check_channel_whitelist(client, message)
	
	# channel blacklisted
	
	if perm["disallow"]:
		return
	
	# strip quotes
	content = sh.rm_leading_quotes(message)
	
	
	if perm["fulltext"]:
		# fulltext search
		for f in f_functions:
			c = getattr(f, "command", False)
			p = getattr(f, "prob", False)
			
			if c and p and re.search(c, content, re.IGNORECASE) and random.random() < p:
				sh.debug("Triggered " + f.__name__ + "...")
				try:
					yield from f(client, message)
				except Exception:
					print("An error occured in " + f.__name__ + "!!! (" + content + ")")
					raise
					continue
	
	# commands
	
	if re.match(client.command_prefix, content):
		sh.debug("This seems to be a command: " + sh.get_command(message))
		
		# check antiflood
		
		if perm["flood"] and ((yield from af.check_flood_channel(client, message)) or (yield from af.check_flood(client, message))):
			sh.debug("Anti-flood kicked in yo")
			return
		
		# help
		
		if re.match(compile_command(r"(help|pomoc)"), content, re.IGNORECASE):
			sh.debug("What a noob")
			ret = "Witam witam, z tej strony Billy Mays z kolejnym fantastycznym produktem!\nDozwolone przedrostki funkcji: . , \ / !\n\n"
			
			for f in c_functions:
				desc = getattr(f, "desc", False)
				
				if hasattr(f, "rhyme") or desc == "hidden":
					continue
					
				command = getattr(f, "command", False)
				
				ret += "." + getattr(f, "command")
				
				params = getattr(f, "params", False);
				
				if params:
					for p in params:
						ret += " [" + p + "]"
				
				if desc:
					ret += " - " + desc
				
				ret += "\n"
			
			ret += "\nRymy i inne bzdety: .rymy"
			ret += "\nZadzwoń teraz, a podwoimy ofertę!"
			
			yield from client.send_message(message.channel, ret)
		
		elif re.match(compile_command(r"(rymy|rhymes)"), content, re.IGNORECASE):
			sh.debug("What an utter pillock")
			ret = "Rymy i inne bzdety:\n"
			
			for f in c_functions:
				if not hasattr(f, "rhyme"):
					continue
				command = getattr(f, "command", False)
				ret += "." + getattr(f, "command") + "\n"
			
			yield from client.send_message(message.channel, ret[:-1])
		
		else:
			# iterate over functions
			for f in c_functions:
				c = getattr(f, "command", False)
				r = re.match(compile_command(c), content, re.IGNORECASE)
				if c and r:
					sh.debug("Executing " + f.__name__ + "...")
					yield from client.send_typing(message.channel)
					try:
						yield from f(client, message)
					except Exception:
						yield from client.send_message(message.channel, "Oho, chyba jakiś błąd w kodzie. <@307949259658100736> to kiedyś naprawi, jak się skończy bawić pociągami.")
						print("An error occured in " + f.__name__ + "!!! (" + content + ")")
						#CZEMU TY CHUJU NIE DZIALASZ
						#logging.exception("An error occured in " + f.__name__ + "!!! (" + content + ")")
						raise
						continue
					break
		
		return
	

# Bot ID
client.run(billy_key)