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
	ret = ""
	dot = True
	
	lines = text.split("\n")
	for line in lines:
		if (line+" ").isspace():
			ret += "\n"
			continue

		insert_flag = False
		tmp = ""
		e = line.split(" ")

		for i in range(100):
			tmp = ""

			for t in e:
				changecase = False
				
				if random.random() < 0.15:
					if dot and t[0].isupper():
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

	if msg.author.id in female_ids:
		return True
	else:
		return False
