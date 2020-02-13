import requests 
import random
import asyncio
import json
import re
import wolframalpha
import ftfy
from bs4 import BeautifulSoup
from cleverwrap import CleverWrap

import time

import billy_shared as sh
from billy_c_translate import translate
from billy_c_yojc import c_rimshot as rimshot
from config import wolfram_key, cleverbot_key

# How many times should the bot retry the query in case an error occurs?
retry_count = 10

cw = CleverWrap(cleverbot_key)

headers_Get = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'
}

def google(q, image=False):
	s = requests.Session()
	q = '+'.join(q.split())
	url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
	if image == "isch":
		url += "&tbm=isch"
	elif image:
		url += "&tbm=isch&tbs=" + image
	
	try:
		r = s.get(url, headers=headers_Get)
	except:
		print("except")
		return False
	 
	soup = BeautifulSoup(r.text, "html.parser")
	
	if image:
		searchWrapper = None
		rules = [{'jsname':'ik8THc'}, {'class':'rg_meta notranslate'}]
		
		hack = False
		
		for rule in rules:
			searchWrapper = soup.findAll('div', rule)
			if len(searchWrapper) != 0:
				break
		
		if len(searchWrapper) == 0:
			hack = True
			searchWrapper = soup.findAll('script')
			json_text = re.sub("AF_initDataCallback.+{return", "", searchWrapper[-2].text).strip()[:-4]
			searchWrapper = json.loads(json_text)[31][0][12][2]
		
		url = None
		
		for result_img in searchWrapper:
			tmp = ""
		
			if hack:
				if result_img[0] == 2:
					continue
				tmp = result_img[1][3][0]
			else:
				tmp = json.loads(result_img.text.strip())["ou"]
			
			banned_terms = ["x-raw-image", "lookaside.fbsbx.com", ".svg"]
			
			if any(term in tmp for term in banned_terms):
				continue
			else:
				url = tmp
				break
		
		if not url:
			return False
		
		if ("wikimedia" in url and "thumb" in url):
			url = re.sub(r"(.+?)(thumb/)(.+)(/.+)", r"\1\3", url)
		elif "wpimg" in url:
			url = re.sub(r"(.+\/\d+x\d+\/)(.+)", r"https://\2", url)
		
		result = {'url': url}
	else:
		searchWrapper = soup.find('div', {'class':'rc'}) #this line may change in future based on google's web page structure
		if searchWrapper is None:
			return False
		url = searchWrapper.find('a')["href"] 
		text = re.sub(r"https?\S+", "", searchWrapper.find('a').text, flags=re.I).strip()
		desc = re.sub(r"https?\S+", "", searchWrapper.find('span', {'class':'st'}).text, flags=re.I).strip()
		result = {'text': text, 'url': url, 'desc' : desc}
	
	return result

def yt(q):
	s = requests.Session()
	q = '+'.join(q.split())
	url = 'https://www.youtube.com/results?search_query=' + q + '&sp=EgIQAQ%253D%253D'
	
	try:
		r = s.get(url, headers=headers_Get)
	except:
		return False
	
	regex = r'\\\"videoId\\\"\:\\\"(\S+?)\\\"'
	ret = re.search(regex, r.text)

	if ret is None:
		regex = r'\"videoId\"\:\"(\S+?)\"'
		ret = re.search(regex, r.text)
	
	if ret is not None:
		result = {'url': 'https://www.youtube.com/watch?v=' + ret.groups()[0]}
	else:
		return False
	
	
	return result

def numerki(q):
    s = requests.Session()
    url = 'https://www.nhentai.net/g/' + q + '/'
	
    try:
        r = s.get(url)
    except:
        return False
		
    parsed = BeautifulSoup(r.text, "html.parser")
    tagi = []
	
    for spa in parsed.findAll('span', {'class': 'tags'}):
        tagi.append(spa.text.strip())

    while("" in tagi) : 
        tagi.remove("")

    #prepare msg
    result = ''

    for tag in tagi :
        result += '[' + tag + ']\n'
		
    return result
	
def tumblr_random(q):
	s = requests.Session()
	url = 'http://'+q+'.tumblr.com/random'
	
	try:
		r = s.get(url, headers=headers_Get)
		if r.url == url:
			return False
		else:
			return r.url
	except:
		return False

def suchar():
	if random.random() < 0.01:
		return "jogurt"
	
	s = requests.Session()
	url = 'http://piszsuchary.pl/losuj'
	
	try:
		r = s.get(url, headers=headers_Get)
	except:
		return False
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	searchWrapper = soup.find('pre', {'class':'tekst-pokaz'})
	if searchWrapper is None:
		return False
	result = searchWrapper.text.strip()[:-17]
	
	return result

def cytat():
	s = requests.Session()
	url = 'http://www.losowe.pl/'
	
	try:
		r = s.get(url, headers=headers_Get)
	except:
		return False
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	searchWrapperC = soup.find('blockquote')
	searchWrapperA = soup.find('div', {'id':'autor'})
	if searchWrapperC is None or searchWrapperA is None:
		return False
	result = {'content' : searchWrapperC.text.strip(), 'author' : searchWrapperA.text.strip()[:-22]}
	
	return result

def bzdur():
	s = requests.Session()
	def joke():
		url = "https://geek-jokes.sameerkumar.website/api"
		try:
			r = s.get(url, headers = headers_Get)
		except:
			return None
		return r.text.strip()[1:-1]
	def basically():
		url = "http://itsthisforthat.com/api.php?text"
		try:
			r = s.get(url, headers = headers_Get)
		except:
			return None
		return r.text.strip()
	def business():
		url = "https://corporatebs-generator.sameerkumar.website/"
		try:
			r = s.get(url, headers = headers_Get)
		except:
			return None
		return json.loads(r.text)["phrase"]
	def advice():
		url = "https://api.adviceslip.com/advice"
		try:
			r = s.get(url, headers = headers_Get)
		except:
			return None
		return json.loads(r.text)["slip"]["advice"]
	result = random.choice([joke, basically, business, advice])()
	return translate(result, out_lang="pl")[0]

def bash():
	s = requests.Session()
	url = 'http://www.losowe.pl/'
	
	try:
		r = s.get(url, headers=headers_Get)
	except:
		return False
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	searchWrapperC = soup.find('blockquote')
	searchWrapperA = soup.find('div', {'id':'autor'})
	if searchWrapperC is None or searchWrapperA is None:
		return False
	result = {'content' : searchWrapperC.text.strip(), 'author' : searchWrapperA.text.strip()[:-22]}
	
	return result

# ---------

@asyncio.coroutine
def c_google(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["text"] + "\n" + result["url"])

c_google.command = r"(g|google)"
c_google.params = ["zapytanie"]
c_google.desc = "szukaj w Google"

@asyncio.coroutine
def c_wyjasnij(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["desc"] + "\n" + result["url"])

c_wyjasnij.command = r"(wyjasnij|explain)"
c_wyjasnij.params = ["zapytanie"]
c_wyjasnij.desc = "szukaj w Google, podaje treść"

@asyncio.coroutine
def c_google_image(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "isch")
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["url"])

c_google_image.command = r"(i|img)"
c_google_image.params = ["zapytanie"]
c_google_image.desc = "szukaj obrazków w Google"


@asyncio.coroutine
def c_google_image_clipart(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "itp:clipart")
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["url"])

c_google_image_clipart.command = r"clipart"
c_google_image_clipart.params = ["zapytanie"]
c_google_image_clipart.desc = "szukaj clipartów"


@asyncio.coroutine
def c_google_image_face(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "itp:face")
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brzydal")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["url"])

c_google_image_face.command = r"(face|twarz)"
c_google_image_face.params = ["zapytanie"]
c_google_image_face.desc = "szukaj obrazków zawierających twarz"


@asyncio.coroutine
def c_google_image_gif(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "itp:animated")
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Google się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["url"])

c_google_image_gif.command = r"gif"
c_google_image_gif.params = ["zapytanie"]
c_google_image_gif.desc = "szukaj animowanych obrazków"

@asyncio.coroutine
def c_wikipedia(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True) + " site:wikipedia.org")
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo Wiki się zesrało.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["text"] + "\n" + result["desc"] + "\n" + result["url"])

c_wikipedia.command = r"(w|wiki?|wikipedia)"
c_wikipedia.params = ["zapytanie"]
c_wikipedia.desc = "szukaj w Wikipedii"


@asyncio.coroutine
def c_youtube(client, message):
	for i in range(retry_count):
		result = yt(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak wyników, albo jutub się zesrał.")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result["url"])

c_youtube.command = r"(yt|youtube)"
c_youtube.params = ["zapytanie"]
c_youtube.desc = "szukaj filmików na YT"


@asyncio.coroutine
def c_numerki(client, message):
	for i in range(retry_count):
		result = numerki(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "brak hentajca, złe numerki?")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result)

c_numerki.command = r"(numerki)"
c_numerki.params = ["zapytanie"]
c_numerki.desc = "wyświetl tagi hentajca po numerkach"

@asyncio.coroutine
def c_tumblr_r(client, message):
	for i in range(retry_count):
		result = tumblr_random(sh.get_args(message))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "wszystko tylko nie to")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result)

#c_tumblr_r.command = r"tumblrr(andom)?"
c_tumblr_r.params = ["tumblr"]
c_tumblr_r.desc = "losowy post z danego Tumblra"


@asyncio.coroutine
def c_zwierzaki(client, message):
	tumblr = random.choice(["fluffy-kittens", "cuteanimals", "cutest-critters"])
	result = tumblr_random(tumblr)
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + "ZJADŁEM WSZYSTKIE KOTY")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result)

#c_zwierzaki.command = r"zwierzaki"
c_zwierzaki.desc = "losowy Tumblr ze zwierzakami"


@asyncio.coroutine
def c_shitpostbot(client, message):
	result = tumblr_random("shitpostbot5k")
	
	if not result:
		yield from client.send_message(message.channel, sh.mention(message) + " I have a crippling depression")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + result)

#c_shitpostbot.command = r"shitpost(bot)?"


@asyncio.coroutine
def c_wolfram(client, message):
	cw = wolframalpha.Client(wolfram_key)
	res = cw.query(sh.get_args(message, True))
	
	if not hasattr(res, "results"):
		yield from client.send_message(message.channel, sh.mention(message) + "nie ma takich rzeczy")
	else:
		yield from client.send_message(message.channel, sh.mention(message) + next(res.results).text)

c_wolfram.command = r"(wa|wolfram)"
c_wolfram.params = ["zapytanie"]
c_wolfram.desc = "Wolfram Alpha"


@asyncio.coroutine
def c_suchar(client, message):
	result = suchar()
	
	if not result:
		yield from client.send_message(message.channel, "jogurt")
	else:
		yield from client.send_message(message.channel, result)
		if random.random() < 0.4:
			yield from rimshot(client, message)

c_suchar.command = r"(suchar|martius)"
c_suchar.desc = "śmiej się razem z nami!"

@asyncio.coroutine
def c_bzdur(client, message):
    result = bzdur()
    if not result:
        yield from client.send_message(message.channel, "Reasumując wszystkie aspekty kwintesencji tematu dochodzę do fundamentalnej konkluzji")
    else:
        yield from client.send_message(message.channel, result)
c_bzdur.command = r"(jacek|jaca|duptysta)"
c_bzdur.desc = "Głębokie teksty głębokiego kolegi"

@asyncio.coroutine
def c_bzdur(client, message):
	result = bzdur()
	if not result:
		yield from client.send_message(message.channel, "Reasumując wszystkie aspekty kwintesencji tematu dochodzę do fundamentalnej konkluzji")
	else:
		yield from client.send_message(message.channel, result)

c_bzdur.command = r"(jacek|jaca|duptysta)"
c_bzdur.desc = "Głębokie teksty głębokiego kolegi"


@asyncio.coroutine
def c_cytat(client, message):
	result = cytat()
	
	if not result:
		yield from client.send_message(message.channel, "Chamsko!\n*~Kathai_Nanjika*")
	else:
		yield from client.send_message(message.channel, result["content"] + "\n*~" + result["author"] + "*")

c_cytat.command = r"cytat"
c_cytat.desc = "życiowe maksymy"


@asyncio.coroutine
def c_cleverbot(client, message):
	yield from client.send_message(message.channel, ftfy.ftfy(sh.mention(message) + cw.say(sh.get_args(message, True))))

c_cleverbot.command = r"(cb|cleverbot|(od)?powiedz|why|(dla)?czego|(dla)?czemu)"
c_cleverbot.params = ["zapytanie"]
c_cleverbot.desc = "spytaj bota o sens życia"


@asyncio.coroutine
def c_cleverbot_reset(client, message):
	cw.reset()

c_cleverbot_reset.command = r"(cb|cleverbot)r(eset)?"
c_cleverbot_reset.desc = "hidden"
