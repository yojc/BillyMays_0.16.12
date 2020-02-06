import random
import asyncio
import itertools
import re
import unidecode

import billy_shared as sh
from billy_antiflood import check_uptime
from billy_nicknames import get_random_nickname

boruc = "Artur Boruc"

@asyncio.coroutine
def c_nickrand(client, message):
	phrase = sh.replace_all(sh.get_args(message), {u'Ą':'A', u'Ę':'E', u'Ó':'O', u'Ś':'S', u'Ł':'L', u'Ż':'Z', u'Ź':'Z', u'Ć':'C', u'Ń':'N', u'ą':'a', u'ę':'e', u'ó':'o', u'ś':'s', u'ł':'l', u'ż':'z', u'ź':'z', u'ć':'c', u'ń':'n'})
	uniq = ''.join(ch for ch, _ in itertools.groupby(''.join(sorted(re.sub("[^a-z]", "", phrase.lower())))))
	uniqV = ''
	uniqC = ''
	uniqN = '0123456789'

	for letter in uniq:
		if letter in "eyuioa":
			uniqV += letter
		else:
			uniqC += letter

	uniqVS = ''.join(random.sample(uniqV,len(uniqV)))
	uniqCS = ''.join(random.sample(uniqC,len(uniqC)))
	uniqNS = ''.join(random.sample(uniqN,len(uniqN)))

	mask = ''
	for letter in phrase:
		if letter.islower():
			mask += 'a'
		elif letter.isupper():
			mask += 'A'
		else:
			mask += '#'

	ret = ''
	for letter in phrase.lower():
		if uniqV.find(letter) > -1:
			ret += uniqVS[uniqV.find(letter)]
		elif uniqC.find(letter) > -1:
			ret += uniqCS[uniqC.find(letter)]
		elif uniqN.find(letter) > -1:
			ret += uniqNS[uniqN.find(letter)]
		else:
			ret += letter

	ret = list(ret)
	for i in range(0, len(ret)):
		if mask[i].islower():
			ret[i] = ret[i].lower()
		elif mask[i].isupper():
			ret[i] = ret[i].upper()

	yield from client.send_message(message.channel, ''.join(ret))

c_nickrand.command = r"rn"
c_nickrand.params = ["zdanie"]
c_nickrand.desc = "Miesza litery w zdaniu"

@asyncio.coroutine
def c_slap(client, message):
	verb = random.choice(['slaps', 'hits', 'smashes', 'beats', 'bashes', 'smacks', 'blasts', 'punches', 'stabs', 'kills', 'decapitates', 'crushes', 'devastates', 'massacres', 'assaults', 'tackles', 'abuses', 'slams', 'slaughters', 'obliderates', 'wipes out', 'pulverizes', 'granulates', 'stuns', 'knocks out', 'strikes', 'bitchslaps', 'scratches', 'pounds', 'bangs', 'whacks', 'rapes', 'eats', 'destroys', 'does nothing to', 'dooms', 'evaporates', 'does something to', 'taunts', 'disrespects', 'disarms', 'mauls', 'dismembers', 'defuses', 'butchers', 'annihilates', 'tortures', 'shatters', 'wrecks', 'toasts', 'dominates', 'suffocates', 'oxidises', 'erases', 'stomps', 'zaps', 'whomps', 'swipes', 'pats', 'nails', 'thumps', '*PAC*'])
	area = random.choice(['around the head', 'viciously', 'repeatedly', 'in the face', 'to death', 'in the balls', 'in the ass', 'savagely', 'brutally', 'infinitely', 'deeply', 'mercilessly', 'randomly', 'homosexually', 'keenly', 'accurately', 'ironically', 'gayly', 'outrageously', 'straight through the heart', 'immediately', 'unavoidably', 'from the inside', 'around a bit', 'from outer space', 'gently', 'silently', 'for real', 'for no apparent reason', 'specifically', 'maybe', 'allegedly', 'once and for all', 'for life', 'stealthly', 'energetically', 'frightfully', 'in the groin', 'in the dignity', 'in the heels', 'in the nostrils', 'in the ears', 'in the eyes', 'in the snout', 'fearfully', 'appallingly', 'vigorously', 'hrabully'])
	size = random.choice(['large', 'huge', 'small', 'tiny', 'enormous', 'massive', 'rusty', 'gay', 'pink', 'sharpened', 'lethal', 'poisoned', 'toxic', 'incredible', 'powerful', 'wonderful', 'priceless', 'explosive', 'rotten', 'smelly', 'puny', 'toy', 'deadly', 'mortal', 'second-rate', 'second-hand', 'otherwise useless', 'magical', 'pneumatic', 'manly', 'sissy', 'iron', 'steel', 'golden', 'filthy', 'semi-automatic', 'invisible', 'infected', 'spongy', 'sharp-pointed', 'undead', 'horrible', 'intimidating', 'murderous', 'intergalactic', 'serious', 'nuclear', 'cosmic', 'mad', 'insane', 'rocket-propelled', 'holy', 'super', 'homosexual', 'imaginary', 'airborne', 'atomic', 'huge', 'lazy', 'stupid', 'communist', 'creepy', 'slimy', 'nazi', 'heavyweight', 'lightweight', 'thin', 'thick'])
	tool = random.choice(['trout', 'fork', 'mouse', 'bear', 'piano', 'cello', 'vacuum', 'mosquito', 'sewing needle', 'nail', 'fingernail', 'opti', 'penis', 'whale', 'cookie', 'straight-arm punch', 'roundhouse kick', 'training shoe', 'dynamite stick', 'Justin Bieber CD', 'fart cloud', 'dildo', 'lightsaber', 'rock', 'stick', 'nigger', 'dinosaur', 'soap', 'foreskin', 'sock', 'underwear', 'herring', 'spider', 'snake', 'ming vase', 'cow', 'jackhammer', 'hammer and sickle', 'razorblade', 'daemon', 'trident', 'gofer', 'alligator', 'bag of piss', 'lobster', 'beer pad', 'toaster', 'printer', 'nailgun', 'banana bomb', 'fetus', 'unicorn statue', 'blood vial', 'electron', 'spell', 'tin of spam', 'behemoth', 'hand grenade', 'hand of God', 'fist of fury', 'erection', 'Pudzian\'s egg kick', 'pimp hand', 'darth fallus', 'dog turd', 'canoe', 'Atari 5200', 'booby trap', 'Gaben', 'fishbot', 'syntax error', 'blue screen of death'])
	
	if sh.get_args(message) == "":
		who = message.author.display_name
	else:
		who = sh.get_args(message)
	
	if who.lower() in ["billy mays", "himself", "self", "billy", "<@312862727385251842>"]:
		who = message.author.display_name
	
	if size[0].lower() in ["a", "e", "i", "o", "u"]:
		witha = "with an";
	else:
		witha = "with a";
	
	action = "*Billy Mays %s %s %s %s %s %s!*" % (verb, who, area, witha, size, tool)
	yield from client.send_message(message.channel, action)

c_slap.command = r"slap"
c_slap.params = ["nick"]


@asyncio.coroutine
def c_pazdzioch(client, message):
	if sh.get_args(message) == "":
		who = message.author.display_name
	else:
		who = sh.get_args(message)
	
	if who.lower() in ["billy mays", "himself", "self", "billy", "<@312862727385251842>"]:
		who = message.author.display_name
	
	what = random.choice(["alkoholik", "analfabeta", "arbuz", "baran", "bambocel", "bezczelny człowiek", "burak", "bydlak nie człowiek", "cham bezczelny", "cham ze wsi spod Elbląga", "chuderlak", "ciemniak", "cymbał", "człowiek kiełbasa", "człowiek niedorozwinięty", "darmozjad", "defekt", "donosiciel", "dupa z uszami", "dureń jeden", "dziad", "dziad kalwaryjski", "dzieciorób", "dzikus", "Einstein zasrany", "erosoman", "frajer", "gagatek", "Gigi Amoroso zasrany", "gnida", "gnój", "głupi psychopata", "głowonóg", "grubas przebrzydły bez czci i wiary", "grubas erosomański", "grubasz pieprzony", "grubas pogański", "grubas pornograficzny", "horror erotyczny", "idiota", "ignorant", "judasz zasrany", "ludożerca", "łobuz", "kanibal", "kapucyn jeden", "kretyn", "krwiożerczy grubas", "menda", "menel", "nędzna karykatura", "nienormalny", "niedorozwój", "nikt", "niewyselekcjonowany burak", "odpad atomowy", "oszust", "pajac", "pasożyt", "parobas", "parówa", "pederasta", "pierdzimąka", "pijak", "pierdoła", "pokraka", "przygłup", "plackarz charytatywny, zasrany", "regularne bydle", "regularny debil i złodziej", "sadysta", "snowboardzista zasrany", "sprośna świnia", "szmaciarz", "świniak", "świnia przebrzydła", "świnia pornograficzna", "świnia zakamuflowana", "świnia żarłoczna", "świnia erosomańska", "śmieć", "taran opasły", "tuman", "ukryty erosoman", "wsza ludzka", "wieprz", "wypierdek", "zagrożenie dla kościoła", "zboczek pieprzony", "zbrodniarz", "zdrajca", "zdewociały faszysta", "znachor zasrany", "żarłoczny, pasożytniczy wrzód na dupie społeczeństwa ludu pracującego miast i wsi"])

	yield from client.send_message(message.channel, "%s to %s!" % (who, what))

c_pazdzioch.command = r"(pazdzioch|boczek)"


@asyncio.coroutine
def c_balls(client, message):
	yield from client.send_message(message.channel, "I've got balls of steel")

c_balls.command = r"balls"
c_balls.desc = "I've got balls of steel"

@asyncio.coroutine
def c_boruc(client, message):
	yield from client.send_message(message.channel, "brawo " + boruc)

c_boruc.command = r"(brawo|boruc)"
c_boruc.desc = "BRAWO ARTUR BORUC"

@asyncio.coroutine
def c_setboruc(client, message):
	global boruc
	
	if sh.get_args(message) == "":
		boruc = "Artur Boruc"
	else:
		boruc = sh.get_args(message)

c_setboruc.command = r"set"
c_setboruc.desc = "hidden"

@asyncio.coroutine
def c_ohgod(client, message):
	yield from client.send_message(message.channel, "oh god oh man")

c_ohgod.command = r"ohgod"
c_ohgod.desc = "Oh god oh man"

@asyncio.coroutine
def c_patch(client, message):
	yield from client.send_message(message.channel, "exec Patch.txt")

c_patch.command = r"patch"
c_patch.desc = "hidden"

@asyncio.coroutine
def c_rimshot(client, message):
	yield from client.send_message(message.channel, "Ba-dum-pish!")

c_rimshot.command = r"rimshot"
c_rimshot.desc = "Ba-dum-pish!"


@asyncio.coroutine
def c_cwiercz(client, message):
	if random.random() < 0.8:
		yield from client.send_message(message.channel, "https://www.youtube.com/watch?v=K8E_zMLCRNg")
	else:
		yield from client.send_message(message.channel, random.choice(["https://www.youtube.com/watch?v=IP5e7jrYBtY", "https://www.youtube.com/watch?v=gmS5yyBrWZU"]))

c_cwiercz.command = r"(cricket(s)?|swierszcz(e)?)"
c_cwiercz.desc = "Używać razem z funkcją .martius"


@asyncio.coroutine
def c_nh(client, message):
	if random.random() < 0.15:
		yield from client.send_message(message.channel, random.choice(["(much homo wow)", "(extra homo)", "(kiceg tier homo)", "(no hetero)", "(yes homo)", "(ecce homo)"]))
	else:
		yield from client.send_message(message.channel, "(no homo)")

c_nh.command = r"(nh|nohomo)"


@asyncio.coroutine
def c_mmmm(client, message):
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

c_mmmm.command = r"m[mh]{2,}"

@asyncio.coroutine
def c_twss(client, message):
	yield from client.send_message(message.channel, "That's what she said!")

c_twss.command = r"twss"
c_twss.desc = "That's what she said!"


@asyncio.coroutine
def c_wybierz(client, message):
	msg = sh.get_args(message)
	if "," in msg:
		delimiter = ","
	else:
		delimiter = " "
	
	tmp = list(filter(None, map(str.strip, msg.split(delimiter))))
	
	if len(tmp) > 0:
		ret = random.choice(tmp)
	else: 
		ret = "nie mam nic do wyboru tłumoku"
	
	yield from client.send_message(message.channel, sh.mention(message) + ret)

c_wybierz.command = r"wybierz"
c_wybierz.params = ["opcja, opcja, opcja..."]


@asyncio.coroutine
def c_ym(client, message):
	yield from client.send_message(message.channel, "Your mom")

c_ym.command = r"ym"
c_ym.desc = "Your mom"


@asyncio.coroutine
def c_esad(client, message):
	yield from client.send_message(message.channel, "Eat shit and die")

c_esad.command = r"esad"
c_esad.desc = "Eat shit and die"


@asyncio.coroutine
def c_kurwa(client, message):
	c = sh.get_command(message).lower()[1:]
	yield from client.send_message(message.channel, sh.mention(message) + sh.insert_word(c, sh.get_args(message)))

c_kurwa.command = r"(kurwa|fucking)"
c_kurwa.params = ["zdanie"]
c_kurwa.desc = "Okrasz wypowiedź wyrafinowanym słownictwem!"


@asyncio.coroutine
def c_wstaw(client, message):
	tmp = sh.get_args(message).split(" ", 1)
	ret = sh.insert_word(tmp[0], tmp[1])
	
	yield from client.send_message(message.channel, sh.mention(message) + ret)

c_wstaw.command = r"(wstaw|insert)"
c_wstaw.params = ["słowo", "zdanie"]
c_wstaw.desc = "Wstaw słowo w dowolne miejsca zdania"


@asyncio.coroutine
def c_uptime(client, message):
	yield from client.send_message(message.channel, check_uptime())

c_uptime.command = r"uptime"
c_uptime.desc = "hidden"


@asyncio.coroutine
def c_pair(client, message):
	if message.server:
		nicks = []
		forbidden = ["Fursik"]
		
		for n in message.server.members:
			if n.display_name not in forbidden:
				nicks.append(n.display_name)
		
		first = random.choice(nicks)
		second = random.choice(nicks)
		
		while first == second:
			second = random.choice(nicks)
		
		yield from client.send_message(message.channel, first + " × " + second)

c_pair.command = r"pair"


@asyncio.coroutine
def c_klocuch(client, message):
	vids = ["https://www.youtube.com/watch?v=YidQZnQSB4I", "https://www.youtube.com/watch?v=Auot04TYZp4", "https://www.youtube.com/watch?v=YJakurmhT-E", "https://www.youtube.com/watch?v=v20aYFWu8f4", "https://www.youtube.com/watch?v=ABhdqD7hGtw", "https://www.youtube.com/watch?v=xhpamcFwRBs", "https://www.youtube.com/watch?v=5itoVUzXHIg", "https://www.youtube.com/watch?v=xLaHAjENWb0", "https://www.youtube.com/watch?v=V77ktdbGmbI", "https://www.youtube.com/watch?v=Q8N_dgvm_28", "https://www.youtube.com/watch?v=CQvBAPMOw1E", "https://www.youtube.com/watch?v=medTXwgrx4U", "https://www.youtube.com/watch?v=BYPR9ebbLFY", "https://www.youtube.com/watch?v=YZI-_MVGRM4", "https://www.youtube.com/watch?v=xq-mD3TCkfc", "https://www.youtube.com/watch?v=E7gCQ6FA3BQ", "https://www.youtube.com/watch?v=09F-waIZG2E", "https://www.youtube.com/watch?v=w1iVTOdllUo", "https://www.youtube.com/watch?v=jn54hyJH1W8", "https://www.youtube.com/watch?v=hN7NZCG63Sk", "https://www.youtube.com/watch?v=gMEWuMmOf-A", "https://www.youtube.com/watch?v=8WFjoBCnzGY", "https://www.youtube.com/watch?v=zii15LcTSLw", "https://www.youtube.com/watch?v=kykPWhAdJZA", "https://www.youtube.com/watch?v=8NV9zyhaQaY", "https://www.youtube.com/watch?v=UrG5mioVZe0", "https://www.youtube.com/watch?v=cJRrqAPyywk", "https://www.youtube.com/watch?v=sccYn-rfq4Q", "https://www.youtube.com/watch?v=EzMkI_FBje0", "https://www.youtube.com/watch?v=YHm60KS0EMc", "https://www.youtube.com/watch?v=s9izhCLWPZs", "https://www.youtube.com/watch?v=qis339gCCSg", "https://www.youtube.com/watch?v=4-wWAtSGSaE", "https://www.youtube.com/watch?v=Ldp0X3SpbnE", "https://www.youtube.com/watch?v=Io3f5bKFlFs", "https://www.youtube.com/watch?v=Ofm-ZU-WbLM", "https://www.youtube.com/watch?v=665_HyoNxU8", "https://www.youtube.com/watch?v=cbm_CikNeEk", "https://www.youtube.com/watch?v=dID0aHDKATU", "https://www.youtube.com/watch?v=Si-L0arYVoE", "https://www.youtube.com/watch?v=xxwJuE215SM", "https://www.youtube.com/watch?v=NG_W3L_iy9w", "https://www.youtube.com/watch?v=AUtNIXO8pcU", "https://www.youtube.com/watch?v=8DDx5r6lwpM", "https://www.youtube.com/watch?v=9QXu7MRCs30", "https://www.youtube.com/watch?v=KUva_V-NWs8", "https://www.youtube.com/watch?v=5Ff1__OBYXc", "https://www.youtube.com/watch?v=TSQnM33CGII", "https://www.youtube.com/watch?v=2k-y5N_vFZA", "https://www.youtube.com/watch?v=NFdhFJ0RzHA", "https://www.youtube.com/watch?v=s0S-Jamzi_c", "https://www.youtube.com/watch?v=fDtCStfL1Y8", "https://www.youtube.com/watch?v=hqt3u3c5QiI", "https://www.youtube.com/watch?v=q1a5TUDISdM", "https://www.youtube.com/watch?v=uZx83buJNA8", "https://www.youtube.com/watch?v=sZg6XSaMAwM", "https://www.youtube.com/watch?v=VurnIaithdo", "https://www.youtube.com/watch?v=acMskgoCacY", "https://www.youtube.com/watch?v=zzRjCjo2SFQ", "https://www.youtube.com/watch?v=LW8YS8jnZxA", "https://www.youtube.com/watch?v=AiPLWSXgGgU", "https://www.youtube.com/watch?v=ZIYnRWfM9sk", "https://www.youtube.com/watch?v=WFgnlaLMbcc", "https://www.youtube.com/watch?v=lfQr68XXCXo", "https://www.youtube.com/watch?v=nwXiFgawbdA", "https://www.youtube.com/watch?v=azvm8A_BIkE", "https://www.youtube.com/watch?v=A_AuB8dXmP4", "https://www.youtube.com/watch?v=XFgMBBwi8lI", "https://www.youtube.com/watch?v=GBSfqEV1cxo", "https://www.youtube.com/watch?v=OoB_clQZJyk", "https://www.youtube.com/watch?v=g0K64KeYyl4", "https://www.youtube.com/watch?v=4UDC3ZpNjlI", "https://www.youtube.com/watch?v=heAtTMF7lzU", "https://www.youtube.com/watch?v=1dsSM1C0f-o", "https://www.youtube.com/watch?v=Ucam4s2rxC4", "https://www.youtube.com/watch?v=HHraFdmGOKQ", "https://www.youtube.com/watch?v=SzBWXg9ns44", "https://www.youtube.com/watch?v=9gzq988ANfg", "https://www.youtube.com/watch?v=_J7zDdQyzPw", "https://www.youtube.com/watch?v=gdLsTCQ3d0s", "https://www.youtube.com/watch?v=sRcHVGTphWY", "https://www.youtube.com/watch?v=UzFj_PrBDDs", "https://www.youtube.com/watch?v=ZL-3-t8hedg", "https://www.youtube.com/watch?v=W_Ro0zlD7x8", "https://www.youtube.com/watch?v=5RGa4lBgEk0", "https://www.youtube.com/watch?v=EChdbKFy5qk", "https://www.youtube.com/watch?v=QdasWOuiB_E", "https://www.youtube.com/watch?v=D_Lyp0jMJS8", "https://www.youtube.com/watch?v=AVHepIx3HXQ"]
	
	yield from client.send_message(message.channel, random.choice(vids))

c_klocuch.command = r"klocuch(12)?"


@asyncio.coroutine
def c_skryba(client, message):
	yield from client.send_message(message.channel, "Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze. Gdybym miał powiedzieć, co cenię w życiu najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi, którzy podali mi pomocną dłoń, kiedy sobie nie radziłem, kiedy byłem sam. I co ciekawe, to właśnie przypadkowe spotkania wpływają na nasze życie. Chodzi o to, że kiedy wyznaje się pewne wartości, nawet pozornie uniwersalne, bywa, że nie znajduje się zrozumienia, które by tak rzec, które pomaga się nam rozwijać. Ja miałem szczęście, by tak rzec, ponieważ je znalazłem. I dziękuję życiu. Dziękuję mu, życie to śpiew, życie to taniec, życie to miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?, skąd czerpiesz tę radość? A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia, że dzisiaj na przykład buduję maszyny, a jutro... kto wie, dlaczego by nie, oddam się pracy społecznej i będę ot, choćby sadzić... znaczy... marchew.")

c_skryba.command = r"skryba"


@asyncio.coroutine
def c_korwin(client, message):
	components = [
		["Proszę zwrócić uwagę, że", "I tak mam trzy razy mniej czasu, więc proszę pozwolić mi powiedzieć:", "Państwo się śmieją, ale", "Ja nie potrzebowałem edukacji seksualnej, żeby wiedzieć, że", "No niestety:", "Gdzie leży przyczyna problemu? Ja państwu powiem:", "Państwo chyba nie wiedzą, że", "Oświadczam kategorycznie:", "Powtarzam:", "Powiedzmy to z całą mocą:", "W polsce dzisiaj", "Państwo sobie nie zdają sprawy, że", "To ja przepraszam bardzo:", "Otóż nie wiem, czy pan*** wie, że", "Yyyyy...", "Ja chcę powiedzieć jedną rzecz:", "Trzeba powiedzieć jasno:", "Jak powiedział wybitny krakowianin Stanisław Lem,", "Proszę mnie dobrze zrozumieć:", "Ja chciałem państwu przypomnieć, że", "Niech państwo nie mają złudzeń:", "Powiedzmy to wyraźnie:"],
		["właściciele niewolników", "związkowcy", "trockiści", "tak zwane dzieci kwiaty", "rozmaici urzędnicy", "federaści", "etatyści", "ci durnie i złodzieje", "ludzie wybrani głosami meneli spod budki z piwem", "socjaliści pobożni", "socjaliści bezbożni", "komuniści z krzyżem w zębach", "agenci obcych służb", "członkowie Bandy Czworga", "pseudo-masoni z Wielkiego Wschodu Francji", "przedstawiciele czerwonej hołoty", "ci wszyscy (tfu!) geje", "funkcjonariusze reżymowej telewizji", "tak zwani ekolodzy", "ci wszyscy (tfu!) demokraci", "agenci bezpieki", "feminazistki"],
		["po przeczytaniu *Manifestu komunistycznego*", "którymi się brzydzę", "których nienawidzę", "z okolic \"Gazety Wyborczej\"", "- czyli taka żydokomuna -", "odkąd zniesiono karę śmierci", "którymi pogardzam", "których miejsce w normalnym kraju jest w więzieniu", "na polecenie Brukseli", "posłusznie", "bezmyślnie", "z nieprawdopodobną pogardą dla człowieka", "za pieniądze podatników", "zgodnie z ideologią LGBTQZ", "za wszelką cenę", "zupełnie bezkarnie", "całkowicie bezczelnie", "o poglądach na lewo od komunizmu", "celowo i świadomie", "z premedytacją", "od czasów Okrągłego Stołu", "w ramach postępu"],
		["udają homoseksualistów", "niszczą rodzinę", "idą do polityki", "zakazują góralom robienia oscypków", "organizują paraolimpiady", "wprowadzają ustrój, w którym raz na cztery lata można wybrać sobie pana", "ustawiają fotoradary", "wprowadzają dotacje", "wydzielają buspasy", "podnosza wiek emerytalny", "rżną głupa", "odbierają dzieci rodzicom", "wprowadzają absurdalne przepisy", "umieszczają dzieci w szkołach koedukacyjnych", "wprowadzają parytety", "nawołują do podniesienia podatków", "próbują skłócić Polskę z Rosją", "głoszą brednie o globalnym ociepleniu", "zakazują posiadania broni", "nie dopuszczają prawicy do władzy", "uczą dzieci homoseksualizmu"],
		["żeby poddawać wszystkich tresurze", "bo taka jest ich natura", "bo chcą wszystko kontrolować", "bo nie rozumieją, że socjalizm nie działa", "żeby wreszcie zapanował socjalizm", "dokładnie tak jak towarzysz Janosik", "zamiast pozwolić ludziom zarabiać", "żeby wyrwać kobiety z domu", "bo to jest w interesie tak zwanych ludzi pracy", "zamiast pozwolić decydować konsumentowi", "żeby nie opłacało się mieć dzieci", "zamiast obniżyć podatki", "bo nie rozumieją, że selekcja naturalna jest czymś dobrym", "żeby mężczyźni przestali być agresywni", "bo dzięki temu mogą brać łapówki", "bo dzięki temu mogą kraść", "bo dostają za to pieniądze", "bo tak się uczy w państwowej szkole", "bo bez tego (tfu!) demokracja nie może istnieć", "bo głupich jest więcej niż mądrych", "bo chcą tworzyć raj na ziemi", "bo chcą niszczyć cywilizację białego człowieka"],
		["co ma zresztą tyle samo sensu, co zawody w szachach dla debili", "co zostało dokładnie zaplanowane w Magdalence przez śp. generała Kiszcaka", "i trzeba być idiotą, żeby ten system popierać", "- ale nawet ja jeszcze dożyję normalnych czasów", "co dowodzi, że wyskrobano nie tych co trzeba", "a zwykłym ludziom wmawiają, że im coś \"dadzą\"", "- cóż - chcieliście (tfu!) demokracji, to macie", "- dlatego trzeba zlikwidować koryto, a nie zmieniać świnie", "a wystarczyłoby przestać wypłacać zaiłki", "podczas gdy normalni ludzie są uważani za dziwaków", "co w wieku XIX po prostu by wysmiano", "- dlatego w społeczeństwie jest równość, a powinno byc rozwarstwienie", "co prowadzi Polskę do katastrofy", "- dlatego trzeba przywrócić normalność", "ale w wolnej Polsce pójdą siedzieć", "przez kolejne kadencje", "o czym się nie mówi", "- i właśnie dlatego Europa umiera", "- ale przyjdą muzułmanie i zrobią porządek", "- tak samo zresztą jak za Hitlera", "- proszę zobaczyć, co się dzieje na Zachodzie, jesli państwo mi nie wierzą", "co sto lat temu nikomu nie przyszłoby nawet do głowy"]
	]
	reply = ""

	for c in components:
		reply += " " + random.choice(c)

	reply += random.choice([".", "!"])

	yield from client.send_message(message.channel, reply)

c_korwin.command = r"korwin"


@asyncio.coroutine
def c_fullwidth(client, message):
	HALFWIDTH_TO_FULLWIDTH = str.maketrans(
		'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~ ',
		'０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～　')
	
	yield from client.send_message(message.channel, unidecode.unidecode(sh.get_args(message, True)).translate(HALFWIDTH_TO_FULLWIDTH))

c_fullwidth.command = r"(fullwidth|fw)"


@asyncio.coroutine
def c_letter_emoji(client, message):
	replacements = [
		(" ", "   "),
		("\(c\)", "©️"),
		("\(r\)", "®️"),
		("\(tm\)", "™️"),
		("cool", "🆒"),
		("free", "🆓"),
		("new", "🆕"),
		("ok", "🆗"),
		("sos", "🆘"),
		("zzz", "💤"),
		("ng", "🆖"),
		("cl", "🆑"),
		("up!", "🆙"),
		("vs", "🆚"),
		("id", "🆔"),
		("ab", "🆎"),
		("<3", "❤"),
		("100", "💯"),
		("a", "🇦"),
		("b", ":b:"),
		("c", "🇨"),
		("d", "🇩"),
		("e", "🇪"),
		("f", "🇫"),
		("g", "🇬"),
		("h", "🇭"),
		("i", "🇮"),
		("j", "🇯"),
		("k", "🇰"),
		("l", "🇱"),
		("m", "🇲"),
		("n", "🇳"),
		("o", "🇴"),
		("p", "🇵"),
		("q", "🇶"),
		("r", "🇷"),
		("s", "🇸"),
		("t", "🇹"),
		("u", "🇺"),
		("v", "🇻"),
		("w", "🇼"),
		("x", "🇽"),
		("y", "🇾"),
		("z", "🇿"),
		("0", ":zero:"),
		("1", ":one:"),
		("2", ":two:"),
		("3", ":three:"),
		("4", ":four:"),
		("5", ":five:"),
		("6", ":six:"),
		("7", ":seven:"),
		("8", ":eight:"),
		("9", ":nine:"),
		("\+", "➕"),
		("-", "➖"),
		("!\?", "⁉"),
		("!!", "‼"),
		("\?", "❓"),
		("!", "❗"),
		("#", ":hash:"),
		("\*", ":asterisk:"),
		("\$", "💲")
	]
	
	ret = unidecode.unidecode(sh.get_args(message, True))
	
	for e in replacements:
		ret = re.sub(e[0], " {} ".format(e[1]), ret, flags=re.I)
	
	yield from client.send_message(message.channel, ret)

c_letter_emoji.command = r"b"


# -------------------------------------
# funkcje używające seed
# -------------------------------------


@asyncio.coroutine
def c_czy(client, message):
	response = ""
	responses_yes = ["tak", "tak", "na pewno", "jeszcze się pytasz?", "tak (no homo)", "zaiste", "teraz już tak", "a czy papież sra w lesie?", "jak najbardziej", "jeszcze jak", "jest możliwe", "owszem", "czemu nie", "no w sumie...", "nom", "w rzeczy samej", "na bank", "skoro tak mówisz, to nie będę zaprzeczał"]
	responses_no = ["nie", "nie", "to mało prawdopodobne", "nie sądzę", "tak (żartuję, hehe)", "no chyba cię pambuk opuścił", "raczej nie", "jeszcze nie", "gówno prawda", "otóż nie", "niep", "akurat", "nawet o tym nie myśl", "bynajmniej", "co ty gadasz", "chyba ty"]
	responses_dunno = ["nie wiem", "być może", "hehe))))))))))))))))))", "może kiedyś", "jeszcze nie wiem", "daj mi chwilę to się zastanowię", "nie wiem, spytaj {}".format(get_random_nickname(message, "genitive")), "tego nawet najstarsi górale nie wiedzą", "a jebnąć ci ciupaską?", "a co ja jestem, informacja turystyczna?"]

	if sh.is_female(message):
		responses_yes = responses_yes + ["tak jest pani kapitan", "trafiłaś w sedno"]
		responses_no = responses_no + ["pani januszko NIE"]
		responses_dunno = responses_dunno + ["nie wiem zarobiony jestem przyjdź Pani jutro", "co za debilka wymyśla te pytania", "nie jesteś za młoda żeby pytać o takie rzeczy?", "sama sobie odpowiedz"]
	else:
		responses_yes = responses_yes + ["tak jest panie kapitanie", "trafiłeś w sedno"]
		responses_no = responses_no + ["panie januszu NIE"]
		responses_dunno = responses_dunno + ["nie wiem zarobiony jestem przyjdź Pan jutro", "co za debil wymyśla te pytania", "nie jesteś za młody żeby pytać o takie rzeczy?", "sam sobie odpowiedz"]
	
	if random.random() < 0.45:
		response = random.choice(responses_yes)
	elif random.random() < (9/11):
		response = random.choice(responses_no)
	else:
		response = random.choice(responses_dunno)
	
	yield from client.send_message(message.channel, sh.mention(message) + response)

c_czy.command = r"czy"
c_czy.params = ["zapytanie"]

@asyncio.coroutine
def c_ile(client, message):
    zeros = random.randint(1,4)
    yield from client.send_message(message.channel, sh.mention(message) + str(random.randint(pow(10, zeros-1), pow(10, zeros))))

c_ile.command = r"(ile|ilu)"
c_ile.params = ["zapytanie"]

@asyncio.coroutine
def c_ocen(client, message):
	ocena = random.randint(1, 10)
	doda = ""
	znak = ""
	if ocena < 10 and ocena > 0:
		doda = random.choice(["", ",5", "-", "+"])
	if ocena > 7:
		znak = random.choice(["", "+ <:znak:391940544458391565>", "- Berlin poleca", ""])
	
	yield from client.send_message(message.channel, sh.mention(message) + str(ocena) + doda + "/10 " + znak)

c_ocen.command = r"ocen"
c_ocen.params = ["zapytanie"]


@asyncio.coroutine
def c_taknie(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(["tak", "nie"]))

c_taknie.command = r"(taknie|tn)"
c_taknie.params = ["zapytanie"]


@asyncio.coroutine
def c_moneta(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(["orzeł", "reszka"]))

c_moneta.command = r"moneta"


@asyncio.coroutine
def c_abcd(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(["a", "b", "c", "d"]))

c_abcd.command = r"abcd"

# -------------------------------------
# kto / kim / komu / kogo
# -------------------------------------

@asyncio.coroutine
def c_gdzie(client, message):
	prefix = ["pod mostem", "w dupie", "na głowie", "na kompie", "w parafii", "w koszu", "w fapfolderze", "na rowerze"]
	suffix = [get_random_nickname(message, "genitive"), "na wydziale elektrycznym", "w Kathowicach", "u Kath w piwnicy", "we Wrocławiu", "w Szczecinie", "w Brwinowie", "w Warszawie", "w Bogatyni", "w Golubiu-Dobrzynie", "w Rzeszowie", "w Krakowie", "w Bydgoszczy", "w Magdalence przy stole z pozostałymi zdrajcami", "tam gdzie stało ZOMO", "na serwerze Interii", "w Gołodupczynie", "w kinie w Berlinie", "w redakcji CD-Action", "naprawdę mnie kusi żeby napisać \"w dupie\"", "w bagażniku Hondy nevki"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(prefix) + " " + random.choice(suffix))

c_gdzie.command = r"gdzie"
c_gdzie.params = ["zapytanie"]

@asyncio.coroutine
def c_kiedy(client, message):
	replies = ["o wpół do dziesiątej rano w Polsce", "wczoraj", "jutro", "jak przyjdą szwedy", "w trzy dni po premierze Duke Nukem Forever 2", "dzień przed końcem świata", "nigdy", "jak dojdą pieniądze", "za godzinkę", "kiedy tylko sobie życzysz", "gdy przestaniesz zadawać debilne pytania", "jak wybiorą czarnego papieża", "już za cztery lata, już za cztery lata", "na sylwestrze u P_aula", "o 3:33", "o 21:37", "jak Kath napisze magisterkę", "jak Dracia zrobi wszystko co musi kiedyś zrobić", "jak nevka wróci na Discorda", "jak Paul wejdzie do platyny", "jak Fel schudnie", "gdy Aiden zgoli rude kudły", "dzień po wybuchowym debiucie Brylanta", "za 12 lat", "gdy Martius przestanie pierdolić o ptakach", "jak podbiel zje mi dupę", "a co ja jestem, informacja turystyczna?", "jak wreszcie wyjebiemy stąd Nargoga", "jak Debiru awansuje do seniora", "jak kanau_fela zamknie FBI", "już tej nocy w twoim łóżku", "jak Strejlau umrze bo jest stary", "nie"]
	
	if sh.is_female(message):
		replies = replies + ["gdy wreszcie znajdziesz chłopaka"]
	else:
		replies = replies + ["gdy wreszcie znajdziesz dziewczynę"]
	
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(replies))

c_kiedy.command = r"kiedy"
c_kiedy.params = ["zapytanie"]

@asyncio.coroutine
def c_kim(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + get_random_nickname(message, "instrumental"))

c_kim.command = r"kim"
c_kim.params = ["zapytanie"]

@asyncio.coroutine
def c_kto(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + get_random_nickname(message, "nominative"))

c_kto.command = r"kto"
c_kto.params = ["zapytanie"]

@asyncio.coroutine
def c_kogo(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + get_random_nickname(message, "accusative"))

c_kogo.command = r"kogo"
c_kogo.params = ["zapytanie"]

@asyncio.coroutine
def c_czyj(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + get_random_nickname(message, "genitive", sh.get_command(message)))

c_czyj.command = r"(czyi(m|mi|ch)|czyj(a|e|ego|ej)?)"
c_czyj.params = ["zapytanie"]

@asyncio.coroutine
def c_komu(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + get_random_nickname(message, "dative"))

c_komu.command = r"komu"
c_komu.params = ["zapytanie"]