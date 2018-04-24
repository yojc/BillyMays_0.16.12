import random
import asyncio

import billy_shared as sh
from billy_c_img import c_wypierdalaj as img_wypierd

# -------------------------------------
# gaywards
# -------------------------------------

@asyncio.coroutine
def f_ohshitimsorry(client, message):
	yield from client.send_message(message.channel, "sorry for what?")

f_ohshitimsorry.command = r'^oh shit,? I(\')?m sorry'
f_ohshitimsorry.prob = 1.0

@asyncio.coroutine
def f_sorryforwhat(client, message):
	yield from client.send_message(message.channel, "our dad told us not to be ashamed of our dicks")

f_sorryforwhat.command = r'^sorry for what'
f_sorryforwhat.prob = 1.0

@asyncio.coroutine
def f_nottobeashamed(client, message):
	yield from client.send_message(message.channel, "especially since they're such good size and all")

f_nottobeashamed.command = r'our dad told us not to be ashamed of our dicks'
f_nottobeashamed.prob = 1.0

@asyncio.coroutine
def f_iseethat(client, message):
	yield from client.send_message(message.channel, "yeah, I see that, daddy gave you good advice")

f_iseethat.command = r'specially since (it(\')?s|theyre|they\'re) such good size'
f_iseethat.prob = 1.0

@asyncio.coroutine
def f_goodadvice(client, message):
	yield from client.send_message(message.channel, "daddy gave you good advice")
	
f_goodadvice.command = r'^yea(h)?(,)? i see that$'
f_goodadvice.prob = 1.0

@asyncio.coroutine
def f_itgetsbigger(client, message):
	yield from client.send_message(message.channel, "it gets bigger when I pull on it")

f_itgetsbigger.command = r'daddy gave you good advice'
f_itgetsbigger.prob = 1.0

@asyncio.coroutine
def f_mmmm(client, message):
	ret = ""
	for x in range(0, random.randint(4, 13)):
		ret += 'm'
	for x in range(0, random.randint(1, 4)):
		ret += 'M'
	for x in range(0, random.randint(2, 5)):
		ret += 'H'
	for x in range(0, random.randint(1, 4)):
		ret += 'M'
	for x in range(0, random.randint(4, 13)):
		ret += 'm'
	yield from client.send_message(message.channel, ret)

f_mmmm.command = r'^it gets bigger when I pull'
f_mmmm.prob = 1.0

@asyncio.coroutine
def f_iriptheskin(client, message):
	yield from client.send_message(message.channel, "sometimes I pull it on so hard, I rip the skin!")

f_iriptheskin.command = r'^m[mh]{9,}'
f_iriptheskin.prob = 1.0

@asyncio.coroutine
def f_mydaddytold(client, message):
	yield from client.send_message(message.channel, "my daddy told me few things too")

f_mydaddytold.command = r'^sometimes I pull it on so hard(,)? I rip the skin'
f_mydaddytold.prob = 1.0

@asyncio.coroutine
def f_nottorip(client, message):
	yield from client.send_message(message.channel, "like, uh, how not to rip the skin by using someone else's mouth")

f_nottorip.command = r'my daddy (told|taught) me few things too'
f_nottorip.prob = 1.0

@asyncio.coroutine
def f_willyoushowme(client, message):
	yield from client.send_message(message.channel, "will you show me?")

f_willyoushowme.command = r'how not to rip the skin by using someone else(\')?s mouth'
f_willyoushowme.prob = 1.0

@asyncio.coroutine
def f_idberighthappy(client, message):
	yield from client.send_message(message.channel, "I'd be right happy to!")

f_idberighthappy.command = r'^will you show me'
f_idberighthappy.prob = 1.0

# -------------------------------------
# funkcje sprawdzające całą wypowiedź
# -------------------------------------

@asyncio.coroutine
def f_cogowno(client, message):
	yield from client.send_message(message.channel, "gówno 1:0")

f_cogowno.command = r'^(co|czo)\b'
f_cogowno.prob = 0.025

@asyncio.coroutine
def f_czyzby(client, message):
	yield from client.send_message(message.channel, "chyba ty")

f_czyzby.command = r'(czyzby|czyżby)'
f_czyzby.prob = 0.05

@asyncio.coroutine
def f_guten(client, message):
	yield from client.send_message(message.channel, "Schwuchtel Arsch in der Nähe!!!")

f_guten.command = r'^guten tag$'
f_guten.prob = 0.5

@asyncio.coroutine
def f_maciek(client, message):
	yield from client.send_message(message.channel, "Maćku")

f_maciek.command = r'^maciek$'
f_maciek.prob = 1.0

@asyncio.coroutine
def f_rucha(client, message):
	yield from client.send_message(message.channel, "ruchasz psa jak sra")

f_rucha.command = r'\.\.\.'
f_rucha.prob = 0.025

@asyncio.coroutine
def f_wulg(client, message):
	yield from client.send_message(message.channel, random.choice(["może byś tak kurwa nie przeklinał", "co?", "bez wulgaryzmów proszę", "na ten kanał zaglądają dzieci", "ostrożniej z językiem", "to kanał PG13", "czy mam ci język uciąć?", "przestań przeklinać gejasie bo cię stąd wypierdolę dyscyplinarnie", "pambuk płacze jak przeklinasz", "mów do mnie brzydko", "Kath bączy jak przeklinasz", "proszę tu nie przeklinać, to porządna knajpa", "nie ma takiego przeklinania chuju", "блять))))))))))", "zamknij pizdę"]))

f_wulg.command = r'(kurw|chuj|pierdol|pierdal|jeb)'
f_wulg.prob = 0.025

@asyncio.coroutine
def f_witam(client, message):
	yield from client.send_message(message.channel, random.choice(["witam na kanale i życzę miłej zabawy", "cześć, kopę lat", "siemanko witam na moim kanale", "witam witam również", "no elo", "salam alejkum", "привет", "dzińdybry", "siemaszki", "serwus", "gitara siema", "dobrý den", "pozdrawiam, " + random.choice(["Piotr Gambal", "Mateusz Handzlik"]), "feedlysiemka " + str(message.author).split("#")[0].lower() + "ox"]))

f_witam.command = r'(witam|cześć|czesc|siema|szalom|joł|shalom|dzi(n|ń)dybry|dzie(n|ń) dobry|siemka)'
f_witam.prob = 0.25

@asyncio.coroutine
def f_opti(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + " uprasza się o nieużywanie słowa \"opti\" na terenie politbiura. Dziękuję.")

f_opti.command = r"opti"
f_opti.prob = 0.05


@asyncio.coroutine
def f_tbh(client, message):
	yield from client.send_message(message.channel, "smh")

f_tbh.command = r"^tbh$"
f_tbh.prob = 1.0


@asyncio.coroutine
def f_smh(client, message):
	yield from client.send_message(message.channel, "tbh")

f_smh.command = r"^smh$"
f_smh.prob = 1.0


@asyncio.coroutine
def f_jakisgolas(client, message):
	replies = ["USUŃ TO", "a bana to byś nie chciał?", "<rzygi>", "ty bamboclu"]
	
	if random.random() < 1/(len(replies)+1):
		yield from client.send_typing(message.channel)
		yield from img_wypierd(client, message)
	else:
		yield from client.send_message(message.channel,  random.choice(replies))

f_jakisgolas.command = r"vkPCjJM.jpg"
f_jakisgolas.prob = 1.0


@asyncio.coroutine
def f_jakisnervo(client, message):
	replies = ["nie", "no chyba nie"]
	
	yield from client.send_message(message.channel,  random.choice(replies))

f_jakisnervo.command = r"(3tsmuxa|We8ms5m).jpg"
f_jakisnervo.prob = 1.0


@asyncio.coroutine
def f_takiezycie(client, message):
	yield from client.send_message(message.channel, "takie życie")

f_takiezycie.command = r"^chamsko"
f_takiezycie.prob = 0.05


#@asyncio.coroutine
#def f_nawzajem(client, message):
#	yield from client.send_message(message.channel, "nawzajem")

#f_nawzajem.command = r"weso(l|ł)"
#f_nawzajem.prob = 1.0