import requests 
import asyncio
import json
import re
import random

import billy_shared as sh

# How many times should the bot retry the query in case an error occurs?
retry_count = 3

def parse_args(msg):
	in_lang = "auto"
	out_lang = "en"
	
	r = re.findall(r"(\:\S+ )", msg)
	
	if len(r) == 2:
		in_lang = r[0][1:-1]
		out_lang = r[1][1:-1]
	elif len(r) == 1:
		out_lang = r[0][1:-1]
	
	return {"msg" : msg[len("".join(re.findall(r"(\:\S+ )", msg))):], "in_lang" : in_lang, "out_lang" : out_lang}


def translate(text, in_lang='auto', out_lang='en', verify_ssl=True):
	raw = False
	if str(out_lang).endswith('-raw'):
		out_lang = out_lang[:-4]
		raw = True

	headers = {
		'User-Agent': 'Mozilla/5.0' +
		'(X11; U; Linux i686)' +
		'Gecko/20071127 Firefox/2.0.0.11'
	}

	query = {
		"client": "gtx",
		"sl": in_lang,
		"source": in_lang,
		"tl": out_lang,
		"dt": "t",
		"q": text,
	}
	url = "http://translate.googleapis.com/translate_a/single"

	for i in range(retry_count):
		#print(str(i) + ", " + in_lang + " => " + out_lang)
		result = requests.get(url, params=query, timeout=9.05, headers=headers,
							verify=verify_ssl).text

		if result == '[,,""]':
			return None, in_lang

		while ',,' in result:
			result = result.replace(',,', ',null,')
			result = result.replace('[,', '[null,')

		try:
			data = json.loads(result)
		except:
			if i == retry_count-1:
				sh.print_warning("\"" + text + "\", " + in_lang + " => " + out_lang, date=True)
				#return -1, result
				return text, False
			else:
				continue

		if raw:
			return str(data), 'en-raw'

		try:
			language = data[2]  # -2][0][0]
		except:
			language = '?'

		return ''.join(x[0] for x in data[0]), language


@asyncio.coroutine
def mangle(client, channel, text, dest="en", randomize=False, original=False):
	langs = ['auto']
	
	if randomize:
		lang_list = "af sq am ar hy az eu bn bs bg ca zh co hr cs da nl eo et fi fr fy gl ka de el gu ht ha iw hi hu is ig id ga it ja jw kn kk km ko ku lo lv lt lb mk mg ms ml mt mi mr mn ne no ny ps fa pt pa ro ru sm gd sr st sn sd si sk sl so es sw sv tl tg ta te th tr uk ur uz vi cy xh yi yo zu".split(" ")
		langs.extend(random.sample(lang_list, 8))
	elif original:
		langs.extend(['en', 'fr', 'de', 'es', 'it'])
	else:
		langs.extend(['fr', 'de', 'es', 'it', 'no', 'he', 'la', 'ja'])
	
	langs.append(dest)
	
	i = 1
	last_lang = langs[0]
	
	while i < len(langs):
		text = translate(text, last_lang, langs[i])

		if text and text[0] is not -1:
			if text[1]:
				last_lang = langs[i]
			text = text[0]
		else:
			yield from client.send_message(channel, sh.dump_errlog_msg(text[1]))
			text = "dupa cycki"
			break
		
		yield from client.send_typing(channel)
		i += 1
	
	return text


# ---------

@asyncio.coroutine
def c_tr(client, message):
	args = parse_args(sh.get_args(message))
	result = translate(args["msg"], args["in_lang"], args["out_lang"])
	
	if result[0] is None:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + "[" + result[1] + " => " + args["out_lang"] + "] " + result[0])

c_tr.command = r"tr"
c_tr.params = [":jęz_wej", ":jęz_wyj", "tekst"]
c_tr.desc = "tłumaczenie (parametry opcjonalne, domyślnie auto => en)"

@asyncio.coroutine
def c_trp(client, message):
	result = translate(sh.get_args(message), "auto", "pl")
	
	if result[0] is None:
		yield from client.send_message(message.channel, sh.mention(message) + "Google nie zna języka śląskiego, proszę tu takich rzeczy nie wklejać.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + "[" + result[1] + " => pl] " + result[0])

c_trp.command = r"trp"
c_trp.params = ["tekst"]
c_trp.desc = "tłumaczenie na j. polski"

@asyncio.coroutine
def c_mangle(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, sh.get_args(message), "en")))

c_mangle.command = r"mangle"
c_mangle.params = [":jęz_wej", ":jęz_wyj", "tekst"]
c_mangle.desc = "najlepsze tłumaczenie (domyślnie auto => en)"

@asyncio.coroutine
def c_manglep(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, sh.get_args(message), "pl")))

c_manglep.command = r"manglep"
c_manglep.params = ["tekst"]
c_manglep.desc = "najlepsze tłumaczenie na polski"

@asyncio.coroutine
def c_mangler(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, sh.get_args(message), "pl", True)))

c_mangler.command = r"mangler"
c_mangler.params = ["tekst"]
c_mangler.desc = "najlepsze tłumaczenie na polski (losowo dobierana kolejność tłumaczeń)"

@asyncio.coroutine
def c_mangleo(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, sh.get_args(message), "pl", False, True)))

c_mangleo.command = r"mangleo"
c_mangleo.params = ["tekst"]
c_mangleo.desc = "najlepsze tłumaczenie na polski (stary algorytm)"

@asyncio.coroutine
def c_manglew(client, message):
	tmp = sh.get_args(message).split(" ", 1)
	ret = sh.insert_word(tmp[0], tmp[1])
	yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, ret, "pl")))

c_manglew.command = r"(manglew|wstaglep)"
c_manglew.params = ["słowo", "zdanie"]
c_manglew.desc = "wstaw + manglep"

@asyncio.coroutine
def c_manglekn(client, message):
	result = translate(sh.get_args(message), "auto", "pl")

	if result[0] is None:
		yield from client.send_message(message.channel, sh.mention(message) + "Google nie zna języka śląskiego, proszę tu takich rzeczy nie wklejać.")
	else:
		text = sh.insert_word("kurwa", result[0]).replace("\n", " ")
		yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, text, "pl")))

c_manglekn.command = r"manglekn"
c_manglekn.params = ["zdanie"]
c_manglekn.desc = "manglep z ekstra dużymi kawałkami wulgaryzmów i bez enterów"

@asyncio.coroutine
def c_manglek(client, message):
	result = translate(sh.get_args(message), "auto", "pl")

	if result[0] is None:
		yield from client.send_message(message.channel, sh.mention(message) + "Google nie zna języka śląskiego, proszę tu takich rzeczy nie wklejać.")
	else:
		text = sh.insert_word("kurwa", result[0])
		yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, text, "pl")))

c_manglek.command = r"manglek"
c_manglek.params = ["zdanie"]
c_manglek.desc = "manglep z ekstra dużymi kawałkami wulgaryzmów"

@asyncio.coroutine
def c_hakan(client, message):
	result = translate(sh.get_args(message), "auto", "pl")

	if result[0] is None:
		yield from client.send_message(message.channel, sh.mention(message) + "Google nie zna języka śląskiego, proszę tu takich rzeczy nie wklejać.")
	else:
		text = sh.insert_word("hakan", result[0])
		yield from client.send_message(message.channel, sh.mention(message) + (yield from mangle(client, message.channel, text, "pl")))

c_hakan.command = r"(al)?haka(n|m)"
c_hakan.params = ["zdanie"]
c_hakan.desc = "manglep z podwójnym Hakkenem na cienkim cieście"
