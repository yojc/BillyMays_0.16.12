import os
import re
import random

testing = False

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
	
	while re.match(r"^[`'\"<]", content):
		oldcontent = content
		content = re.sub(r"^```[\S\s]+?```", "", content)
		content = re.sub(r"^``[\S\s]+?``", "", content)
		content = re.sub(r"^`[\S\s]+?`", "", content)
		content = re.sub(r"^'[\S\s]+?'", "", content)
		content = re.sub(r"^\"[\S\s]+?\"", "", content)
		content = re.sub(r"^\"[\S\s]+?\"", "", content)
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
	return rm_leading_quotes(msg).split(None, 1)[0]

def generate_seed(input):
	return ''.join(ch for ch, _ in itertools.groupby(''.join(sorted(re.sub("[^a-z0-9]", "", replace_all(input, {u'Ą':'A', u'Ę':'E', u'Ó':'O', u'Ś':'S', u'Ł':'L', u'Ż':'Z', u'Ź':'Z', u'Ć':'C', u'Ń':'N', u'ą':'a', u'ę':'e', u'ó':'o', u'ś':'s', u'ł':'l', u'ż':'z', u'ź':'z', u'ć':'c', u'ń':'n'}).lower())[3:]))))

def file_path(file):
	return os.path.dirname(os.path.abspath(__file__)) + "/" + file

def replace_all(text, dic):
	for i, j in iter(dic.items()):
		text = text.replace(i, j)
	return text

def insert_word(c, text):
	e = text.split(" ")
	ret = ""
	dot = True
	
	for t in e:
		changecase = False
		
		if random.random() < 0.2:
			if dot and t[0].isupper():
				ret += c.title() + " "
				if t.istitle():
					changecase = True
			else:
				ret += c + " "
		
		if t.endswith("."):
			dot = True
		else:
			dot = False
		
		if changecase:
			ret += t.lower() + " "
		else:
			ret += t + " "
	
	return ret
