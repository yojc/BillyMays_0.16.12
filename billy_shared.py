import os
import re
import random
import json
import time
from imp import find_module
from config import bot_owners

# Debug messages flag
testing = False

# List of imported bot functions, only relevant in --stats mode
function_list = None
function_list_modified = None

def set_debug_flag():
	global testing
	testing = True

who_prefixes = ("o ", "z ", "u ", "na ", "za ", "od ", "do ", "w ")

try:
	find_module('colorama')
	from colorama import Fore, Style, init as colorama_init
	colorama_init()
	def print_warning(text, date=False):
		if date:
			print(Fore.YELLOW + Style.BRIGHT + time.strftime("%Y-%m-%d %H:%M:%S") + " " + text + Style.RESET_ALL)
		else:
			print(Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL)
except ImportError:
	def print_warning(text, date=False):
		if date:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + text)
		else:
			print(text)
	print_warning("Colorama library not installed, errors won't be colorized")

# Utilities

def debug(msg, obj=False):
	if testing:
		if obj != False:
			print((msg + " [author: {}; channel: {}; time: {}]".format(str(obj.author), str(obj.channel), str(obj.timestamp))).strip(" "))
		else:
			print(msg)

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except ValueError as e:
		return False
	return True

# File I/O

def file_path(file):
	return os.path.dirname(os.path.abspath(__file__)) + "/" + file

def dump_errlog(content):
	logfilename = time.strftime("%Y-%m-%d_%H-%M-%S.txt")
	with open(file_path("errlog/" + logfilename), "w") as logfile:
		logfile.write(content)
	
	return logfilename

def list_modules(dev=False):
	ret = []
	for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		dev_module = dev and file.startswith("billy_c_dev_")
		prod_module = not dev and not file.startswith("billy_c_dev_") and file.startswith("billy_c_") and file != "billy_c_stats.py"
		if file.endswith(".py") and (dev_module or prod_module):
			ret.append(file.rstrip(".py"))
	return ret

def dump_function_names(arr):
	debug("Dumping function list to disk")
	db_path = file_path("billy_db_functions.db")

	with open(db_path, "w") as db:
		data = {}
		for f in arr:
			data[f.__name__] = getattr(f, "command", False)
		
		json.dump(data, db)

def import_function_names():
	db_path = file_path("billy_db_functions.db")

	if os.path.exists(db_path):
		with open(db_path, "r") as db:
			try:
				data = json.load(db)
			except:
				data = {}
	else:
		data = {}
	
	return data

def get_function_names():
	global function_list
	global function_list_modified

	# Update every 24h
	if not function_list or (function_list_modified - time.monotonic() > 60 * 60 * 24):
		debug("Reading function list from disk")
		function_list = import_function_names()
		function_list_modified = time.monotonic()
	
	return function_list

# Messages

def dump_errlog_msg(content):
	return "Ojoj, chyba serwer mi po śląsku odpowiedział. <@" + bot_owners[0] + "> gamoniu sprawdź plik " + dump_errlog(content)

def check_dest(msg):
	if str(msg.channel).startswith("Direct Message"):
		return msg.author
	else:
		return msg.channel
	

def mention(msg):
	return msg.author.mention + ": "

def replace_all(text, dic):
	for i, j in iter(dic.items()):
		text = text.replace(i, j)
	return text
	return msg.author.mention + ": "

def rm_leading_quotes(msg, clean = False):
	if clean:
		content = msg.clean_content
	else:
		content = msg.content
	
	while re.match(r"^[`'\"<>]", content):
		oldcontent = content
		content = re.sub(r"^```[\S\s]+?```", "", content)
		content = re.sub(r"^``[\S\s]+?``", "", content)
		content = re.sub(r"^`[\S\s]+?`", "", content)
		content = re.sub(r"^'[\S\s]+?'", "", content)
		content = re.sub(r"^\"[\S\s]+?\"", "", content)
		content = re.sub(r"^>[\S\s]+?\n", "", content)
		content = re.sub(r"^<[\S\s]+?>", "", content).strip()
		
		if oldcontent == content:
			break
	
	return content

def get_args(msg, clean = False):
	tmp = rm_leading_quotes(msg, clean).split(None, 1)
	if len(tmp) > 1:
		return tmp[1].strip()
	else:
		return ""

def get_command(msg):
	msg_strip = rm_leading_quotes(msg)[1:]

	if msg_strip.startswith(who_prefixes):
		tmp = msg_strip.split(None, 2)
		return tmp[0] + " " + tmp[1]
	else:
		try:
			return msg_strip.split(None, 2)[0]
		except Exception:
			print_warning(msg_strip)
			return None

def is_female(msg):
	female_ids = ["227096453552668673", "138007616700809216", "178592536795938818", "352111453169254400", "401821271371022355", "383653815334862858", "388014310359826433", "175879138219917312", "384783502396358658"]
	if hasattr(msg, "author"):
		user_id = msg.author.id
	else: 
		user_id = msg.id

	if user_id in female_ids:
		return True
	else:
		return False

# Other

def generate_seed(input):
	return ''.join(ch for ch, _ in itertools.groupby(''.join(sorted(re.sub("[^a-z0-9]", "", replace_all(input, {u'Ą':'A', u'Ę':'E', u'Ó':'O', u'Ś':'S', u'Ł':'L', u'Ż':'Z', u'Ź':'Z', u'Ć':'C', u'Ń':'N', u'ą':'a', u'ę':'e', u'ó':'o', u'ś':'s', u'ł':'l', u'ż':'z', u'ź':'z', u'ć':'c', u'ń':'n'}).lower())[3:]))))

def insert_word(c, text):
	ret = ""
	dot = True
	
	lines = re.sub(' +', ' ', text).split("\n")
	for line in lines:
		if (line+" ").isspace():
			ret += "\n"
			continue

		insert_flag = False
		tmp = ""
		e = line.strip().split(" ")

		for i in range(100):
			tmp = ""

			for t in e:
				changecase = False
				
				if random.random() < 0.15:
					if dot and len(t) > 0 and t[0].isupper():
						tmp += c.title() + " "
						if t.istitle():
							changecase = True
					else:
						tmp += c + " "
					
					insert_flag = True
				
				if t.endswith("."):
					dot = True
				else:
					dot = False
				
				if changecase:
					tmp += t.lower() + " "
				else:
					tmp += t + " "
			
			if insert_flag or i==99:
				ret += tmp + "\n"
				break
	
	return ret.strip()

def replace_all(text, dic):
	for i, j in iter(dic.items()):
		text = text.replace(i, j)
	return text