import os
import re
import random
from imp import find_module

testing = False

try:
	find_module('colorama')
	from colorama import Fore, Style, init as colorama_init
	colorama_init()
	def print_warning(text):
		print(Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL)
except ImportError:
	def print_warning(text):
		print(text)
	print_warning("Colorama library not installed, errors won't be colorized")

def debug(msg, obj=False):
	if testing:
		if obj != False:
			print(msg + " [author: {}; channel: {}; time: {}]".format(str(obj.author), str(obj.channel), str(obj.timestamp)))
		else:
			print(msg)

def check_dest(msg):
	if str(msg.channel).startswith("Direct Message"):
		return msg.author
	else:
		return msg.channel
	

def mention(msg):
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
		return tmp[1]
	else:
		return ""

def get_command(msg):
	msg_strip = rm_leading_quotes(msg)[1:]

	if msg_strip.startswith(("o ", "z ", "u ")):
		tmp = msg_strip.split(None, 2)
		return tmp[0] + " " + tmp[1]
	else:
		return msg_strip.split(None, 2)[0]

def generate_seed(input):
	return ''.join(ch for ch, _ in itertools.groupby(''.join(sorted(re.sub("[^a-z0-9]", "", replace_all(input, {u'Ą':'A', u'Ę':'E', u'Ó':'O', u'Ś':'S', u'Ł':'L', u'Ż':'Z', u'Ź':'Z', u'Ć':'C', u'Ń':'N', u'ą':'a', u'ę':'e', u'ó':'o', u'ś':'s', u'ł':'l', u'ż':'z', u'ź':'z', u'ć':'c', u'ń':'n'}).lower())[3:]))))

def file_path(file):
	return os.path.dirname(os.path.abspath(__file__)) + "/" + file

def replace_all(text, dic):
	for i, j in iter(dic.items()):
		text = text.replace(i, j)
	return text

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
