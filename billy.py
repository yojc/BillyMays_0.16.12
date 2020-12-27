# Modules to import
python_modules = [
	"discord", 
	"asyncio",
	"platform",
	
	"sys",
	"argparse",
	"random",
	"re",
	"datetime",
	"emoji",
	"unidecode",
	"signal"
	]

for m in python_modules:
	globals()[m] = __import__(m)

# Bot dependencies
from discord.ext.commands import Bot
from discord.ext import commands

# Read command line arguments
parser = argparse.ArgumentParser(description="Just some Discord bot.")
parser.add_argument("-b", "--debug", help="enable simple debug messages", action="store_true")
parser.add_argument("-l", "--list", help="list all imported functions on startup", action="store_true")
parser.add_argument("-n", "--nostats", help="startup mode: disabled statistics module", action="store_true")
parser.add_argument("-s", "--stats", help="startup mode: statistics module ONLY", action="store_true")
parser.add_argument("-d", "--dev", help="startup mode: developer. Disables all modules (except billy_c_dev_*.py) and applies --list and --debug. Accepts commands only from bot owner(s). All functions use dev_ prefix! (eg. .dev_help)", action="store_true")

args = parser.parse_args()

NOSTATS_MODE = args.nostats
STATS_MODE = args.stats
DEBUG_MODE = args.debug
DEV_MODE = args.dev
LIST_FUNCTIONS = args.list

if DEV_MODE and (NOSTATS_MODE or STATS_MODE):
	print("Developer mode is meant to be used as a standalone parameter")
	sys.exit(2)
elif NOSTATS_MODE and STATS_MODE:
	print("--nostats and --stats are mutually exclusive")
	sys.exit(2)

# App keys
from config import billy_key, bot_owners

# Shared functions

import billy_antiflood as af
import billy_shared as sh

if DEV_MODE or DEBUG_MODE:
	sh.set_debug_flag()

if STATS_MODE:
	sh.print_warning("Stats collection mode only enabled!")
elif NOSTATS_MODE:
	sh.print_warning("Stats module is completely disabled!")
elif DEV_MODE:
	# Import all modules starting with billy_c_dev
	for m in sh.list_modules(dev=True):
		globals()[m] = __import__(m)

	sh.print_warning("DEVELOPER MODE ENABLED!")

if DEBUG_MODE and not DEV_MODE:
	sh.print_warning("Debug info enabled!")

# Import all modules starting with billy_c

if not (DEV_MODE or STATS_MODE):
	for m in sh.list_modules():
		globals()[m] = __import__(m)

if not (DEV_MODE or NOSTATS_MODE):
	import billy_c_stats
else:
	# Ugly hack, don't look
	billy_c_stats = None


print("--------")

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

# To prevent multiple reminder setup
sopel_reminder_setup = False

def compile_command(regex):
	return client.command_prefix + ("dev_" if DEV_MODE else "") + regex + r"\b"

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
						sh.print_warning("Invalid specified time: " + name)
						continue
					elif not hasattr(val, "channels"):
						sh.print_warning("No channels specified: " + name)
						continue
					else:
						# Timer functions functions
						if (DEV_MODE or LIST_FUNCTIONS):
							sh.debug("Imported timer: " + name)
						t_functions.append(val)
						i += 1
				
				elif not hasattr(val, "command"):
					# Omit functions without specified .command
					sh.print_warning("Missing command regex: " + name)
					continue
				
				elif name.startswith("f_") and not hasattr(val, "prob"):
					# Omit fulltext without specified .prob
					sh.print_warning("Missing fulltext probability: " + name)
					continue
				
				elif name.startswith("c_"):
					# Called functions
					if (DEV_MODE or LIST_FUNCTIONS):
						sh.debug("Imported command: " + name)
					c_functions.append(val)
					i += 1
				
				elif name.startswith("f_"):
					# Fulltext search
					if (DEV_MODE or LIST_FUNCTIONS):
						sh.debug("Imported fulltext: " + name)
					f_functions.append(val)
					i += 1
			
		print("Loaded " + str(i) + " functions from module " + module_name)
	else:
		if module_name not in python_modules:
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
			
			if (not t and interval != 30):
				yield from fun(client, channels)
			elif (not fun.__name__ in current_day or current_day[fun.__name__] != now.day) and (not t or (t[0] == now.hour and t[1] == now.minute)):
				current_day[fun.__name__] = now.day
				yield from fun(client, channels)
			
			yield from asyncio.sleep(interval)
	
	client.loop.create_task(f(e))

# Parse message and execute functions

@asyncio.coroutine
def parse_message(message, edited=False):
	if DEV_MODE and message.author.id not in bot_owners:
		#sh.debug("Received and ignored a message")
		return

	if not (DEV_MODE or NOSTATS_MODE):
		if not edited:
			billy_c_stats.insert_msg(message)
		
		# Track used emojis
		
		emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
		custom_emoji_list = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
		billy_c_stats.insert_emojis_post(message, emoji_list, custom_emoji_list, edited)
	
	# Ignore bot messages
	
	if message.author == client.user:
		return
	
	perm = af.check_channel_whitelist(client, message)
	
	# Channel blacklisted
	
	if perm["disallow"]:
		return
	
	# Strip quotes
	content = unidecode.unidecode(sh.rm_leading_quotes(message))
	
	
	if not edited:
		# Fulltext search
		for f in f_functions:
			c = getattr(f, "command", False)
			p = getattr(f, "prob", False)
			
			if c and p and re.search(c, content, re.IGNORECASE) and (p >= 1.0 or (perm["fulltext"] and random.random() < p)):
				sh.debug("Triggered " + f.__name__ + "...")
				try:
					yield from f(client, message)
				except Exception:
					sh.print_warning("An error occured in " + f.__name__ + "!!! (" + content + ")")
					raise
					
	# Commands
	
	if re.match(client.command_prefix, content):
		sh.debug("This seems to be a command: ." + sh.get_command(message))
		
		# Check antiflood
		
		if not (STATS_MODE or DEV_MODE) and perm["flood"] and ((yield from af.check_flood_channel(client, message)) or (yield from af.check_flood(client, message))):
			sh.debug("Anti-flood kicked in yo")
			return
		
		# Help
		
		if not STATS_MODE and re.match(compile_command(r"(help|pomoc)"), content, re.IGNORECASE):
			ret = "Witam witam, z tej strony Billy Mays z kolejnym fantastycznym produktem!\nDozwolone przedrostki funkcji: . , \ / ! ;\n\n"
			
			for f in c_functions:
				desc = getattr(f, "desc", False)
				
				if hasattr(f, "rhyme") or desc == "hidden":
					continue
					
				command = getattr(f, "command", False)
				
				ret += "." + getattr(f, "command")
				
				params = getattr(f, "params", False)
				
				if params:
					for p in params:
						ret += " [" + p + "]"
				
				if desc:
					ret += " - " + desc
				
				ret += "\n"
			
			ret += "\nRymy i inne bzdety: .rymy"
			ret += "\nZadzwoń teraz, a podwoimy ofertę!"
			
			if len(ret) > 2000:
				n = 40
				groups = ret.split("\n")
				help = ["\n".join(groups[:n]), "\n".join(groups[n:n*2]), "\n".join(groups[n*2:])]
			else:
				help = [ret]
			
			for m in help:
				yield from client.send_message(message.channel, m)
		
		elif not STATS_MODE and re.match(compile_command(r"(rymy|rhymes)"), content, re.IGNORECASE):
			ret = "Rymy i inne bzdety:\n"
			
			for f in c_functions:
				if not hasattr(f, "rhyme"):
					continue
				command = getattr(f, "command", False)
				ret += "." + getattr(f, "command") + "\n"
			
			yield from client.send_message(message.channel, ret[:-1])
		
		else:
			# Iterate over functions
			for f in c_functions:
				c = getattr(f, "command", False)
				r = re.match(compile_command(c), content, re.IGNORECASE)
				if c and r:
					sh.debug("Executing " + f.__name__ + "...")
					yield from client.send_typing(message.channel)

					try:
						yield from f(client, message)

						if not (NOSTATS_MODE or DEV_MODE):
							billy_c_stats.update_msg_function(message, f.__name__)
					except Exception:
						yield from client.send_message(message.channel, "Oho, chyba jakiś błąd w kodzie. <@" + bot_owners[0] + "> to kiedyś naprawi, jak się skończy bawić pociągami.")
						sh.print_warning("An error occured in " + f.__name__ + "!!! (" + content + ")")
						#CZEMU TY CHUJU NIE DZIALASZ
						#logging.exception("An error occured in " + f.__name__ + "!!! (" + content + ")")
						raise
						continue
					break
			
			# If stats mode only: import function names from database
			if STATS_MODE:
				for f in sh.get_function_names():
					c = sh.function_list[f]
					r = re.match(compile_command(c), content, re.IGNORECASE)
					if c and r:
						sh.debug("Adding " + f + " to stat database...")
						try:
							billy_c_stats.update_msg_function(message, f)
						except Exception:
							sh.print_warning("Stat database msg update error " + f + "!!! (" + content + ")")
							raise
							continue
						break


# Sort functions alphabetically (for .help)
c_functions.sort(key=lambda x: x.__name__)

# Dump function names to file
if not (STATS_MODE or DEV_MODE):
	sh.dump_function_names(c_functions)

print("--------")

# Start the bot and display startup info
@client.event
@asyncio.coroutine
def on_ready():
	global sopel_reminder_setup
	
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('Connection datetime: ' + str(datetime.datetime.now()))
	print('--------')
	sh.debug('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	sh.debug('--------')
	#print('Use this link to invite {}:'.format(client.user.name))
	#print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	#print('--------')
	
	if not (DEV_MODE or STATS_MODE) and not sopel_reminder_setup:
		sh.debug("### CREATED REMINDER TASKS " + str(datetime.datetime.now()))
		sopel_reminder_setup = True
		yield from billy_c_sopel_remind.setup(client)
	elif DEV_MODE:
		sh.debug("### REMINDERS DISABLED IN DEVELOPER MODE")
	else:
		sh.debug("### REMINDERS ALREADY ACTIVE")
		


# Execute on every reaction

@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
	if reaction.me:
		return
	elif not (NOSTATS_MODE or DEV_MODE):
		# Track used emojis
		billy_c_stats.insert_emojis_reaction(reaction.message, user, reaction.emoji, reaction.custom_emoji)
	
	#if random.random() < 0.001:
	#	yield from asyncio.sleep(4)
	#	yield from client.add_reaction(reaction.message, reaction.emoji)

@client.event
@asyncio.coroutine
def on_reaction_remove(reaction, user):
	if not (NOSTATS_MODE or DEV_MODE):
		# Track used emojis
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
	if not (NOSTATS_MODE or DEV_MODE):
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

@client.event
@asyncio.coroutine
def on_member_join(member):
	if not (NOSTATS_MODE or DEV_MODE):
		invitation_msg = "Witam witam {} na naszym magicznym serwerze!".format(member.mention)
		
		if member.server.id == "174449535811190785":
			yield from client.send_file(member.server.default_channel, sh.file_path("img/w mcdonalds spotkajmy sie.jpg"), content=invitation_msg)
			yield from client.send_message(member.server.default_channel, "(lepiej nie pytaj kto to jest)")
		else:
			yield from client.send_message(member.server.default_channel, invitation_msg)

@client.event
@asyncio.coroutine
def on_member_remove(member):
	if not (NOSTATS_MODE or DEV_MODE):
		word = "polazła" if sh.is_female(member) else "polazł"
		
		yield from client.send_message(member.server.default_channel, "{} ({}) właśnie se stąd gdzieś {} <:smaglor:328947669676457984>".format(member.mention, str(member), word))

# Bot ID
client.run(billy_key)

# Catch SIGINT
def signal_handler(sig, frame):
	print("SIGINT CAUGHT MOFO")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)