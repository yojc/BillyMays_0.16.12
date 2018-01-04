import requests 
import asyncio
import json
import re

import billy_shared as sh

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
		"tl": out_lang,
		"dt": "t",
		"q": text,
	}
	url = "http://translate.googleapis.com/translate_a/single"
	result = requests.get(url, params=query, timeout=40, headers=headers,
						  verify=verify_ssl).text

	if result == '[,,""]':
		return None, in_lang

	while ',,' in result:
		result = result.replace(',,', ',null,')
		result = result.replace('[,', '[null,')

	data = json.loads(result)

	if raw:
		return str(data), 'en-raw'

	try:
		language = data[2]  # -2][0][0]
	except:
		language = '?'

	return ''.join(x[0] for x in data[0]), language


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
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + "[" + result[1] + " => pl] " + result[0])

c_trp.command = r"trp"
c_trp.params = ["tekst"]
c_trp.desc = "tłumaczenie na j. polski"

@asyncio.coroutine
def c_mangle(client, message):
	args = parse_args(sh.get_args(message))
	text = args["msg"]
	langs = [args["in_lang"], 'fr', 'de', 'es', 'it', 'no', 'he', 'la', 'ja', args["out_lang"]]
	i = 1
	
	while i < len(langs):
		text = translate(text, langs[i-1], langs[i])[0]
		yield from client.send_typing(message.channel)
		i += 1
	
	if text is None:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + text)

c_mangle.command = r"mangle"
c_mangle.params = [":jęz_wej", ":jęz_wyj", "tekst"]
c_mangle.desc = "najlepsze tłumaczenie (domyślnie auto => en)"

@asyncio.coroutine
def c_manglep(client, message):
	text = sh.get_args(message)
	langs = ['auto', 'fr', 'de', 'es', 'it', 'no', 'he', 'la', 'ja', 'en', 'pl']
	i = 1
	
	while i < len(langs):
		text = translate(text, langs[i-1], langs[i])[0]
		yield from client.send_typing(message.channel)
		i += 1
	
	if text is None:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + text)

c_manglep.command = r"manglep"
c_manglep.params = ["tekst"]
c_manglep.desc = "najlepsze tłumaczenie na polski"