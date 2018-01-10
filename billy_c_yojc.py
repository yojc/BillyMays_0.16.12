import random
import asyncio
import itertools
import re

import billy_shared as sh
from billy_antiflood import check_uptime

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


def c_slap(client, message):
	verb = random.choice(['slaps', 'hits', 'smashes', 'beats', 'bashes', 'smacks', 'blasts', 'punches', 'stabs', 'kills', 'decapitates', 'crushes', 'devastates', 'massacres', 'assaults', 'tackles', 'abuses', 'slams', 'slaughters', 'obliderates', 'wipes out', 'pulverizes', 'granulates', 'stuns', 'knocks out', 'strikes', 'bitchslaps', 'scratches', 'pounds', 'bangs', 'whacks', 'rapes', 'eats', 'destroys', 'does nothing to', 'dooms', 'evaporates', 'does something to', 'taunts', 'disrespects', 'disarms', 'mauls', 'dismembers', 'defuses', 'butchers', 'annihilates', 'tortures', 'shatters', 'wrecks', 'toasts', 'dominates', 'suffocates', 'oxidises', 'erases', 'stomps', 'zaps', 'whomps', 'swipes', 'pats', 'nails', 'thumps', '*PAC*'])
	area = random.choice(['around the head', 'viciously', 'repeatedly', 'in the face', 'to death', 'in the balls', 'in the ass', 'savagely', 'brutally', 'infinitely', 'deeply', 'mercilessly', 'randomly', 'homosexually', 'keenly', 'accurately', 'ironically', 'gayly', 'outrageously', 'straight through the heart', 'immediately', 'unavoidably', 'from the inside', 'around a bit', 'from outer space', 'gently', 'silently', 'for real', 'for no apparent reason', 'specifically', 'maybe', 'allegedly', 'once and for all', 'for life', 'stealthly', 'energetically', 'frightfully', 'in the groin', 'in the dignity', 'in the heels', 'in the nostrils', 'in the ears', 'in the eyes', 'in the snout', 'fearfully', 'appallingly', 'vigorously', 'hrabully'])
	size = random.choice(['large', 'huge', 'small', 'tiny', 'enormous', 'massive', 'rusty', 'gay', 'pink', 'sharpened', 'lethal', 'poisoned', 'toxic', 'incredible', 'powerful', 'wonderful', 'priceless', 'explosive', 'rotten', 'smelly', 'puny', 'toy', 'deadly', 'mortal', 'second-rate', 'second-hand', 'otherwise useless', 'magical', 'pneumatic', 'manly', 'sissy', 'iron', 'steel', 'golden', 'filthy', 'semi-automatic', 'invisible', 'infected', 'spongy', 'sharp-pointed', 'undead', 'horrible', 'intimidating', 'murderous', 'intergalactic', 'serious', 'nuclear', 'cosmic', 'mad', 'insane', 'rocket-propelled', 'holy', 'super', 'homosexual', 'imaginary', 'airborne', 'atomic', 'huge', 'lazy', 'stupid', 'communist', 'creepy', 'slimy', 'nazi', 'heavyweight', 'lightweight', 'thin', 'thick'])
	tool = random.choice(['trout', 'fork', 'mouse', 'bear', 'piano', 'cello', 'vacuum', 'mosquito', 'sewing needle', 'nail', 'fingernail', 'opti', 'penis', 'whale', 'cookie', 'straight-arm punch', 'roundhouse kick', 'training shoe', 'dynamite stick', 'Justin Bieber CD', 'fart cloud', 'dildo', 'lightsaber', 'rock', 'stick', 'nigger', 'dinosaur', 'soap', 'foreskin', 'sock', 'underwear', 'herring', 'spider', 'snake', 'ming vase', 'cow', 'jackhammer', 'hammer and sickle', 'razorblade', 'daemon', 'trident', 'gofer', 'alligator', 'bag of piss', 'lobster', 'beer pad', 'toaster', 'printer', 'nailgun', 'banana bomb', 'fetus', 'unicorn statue', 'blood vial', 'electron', 'spell', 'tin of spam', 'behemoth', 'hand grenade', 'hand of God', 'fist of fury', 'erection', 'Pudzian\'s egg kick', 'pimp hand', 'darth fallus', 'dog turd', 'canoe', 'Atari 5200', 'booby trap', 'Gaben', 'fishbot', 'syntax error', 'blue screen of death'])
	
	if sh.get_args(message) == "":
		who = message.author.display_name
	else:
		who = sh.get_args(message)
	
	if who.lower() == "Billy Mays".lower() or who.lower() == "himself":
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
	if random.random() < 0.1:
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

c_mmmm.command = r"m{3,}"

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
def c_kurwa(client, message):
	c = sh.get_command(message).lower()[1:]
	e = sh.get_args(message).split(" ")
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
	
	yield from client.send_message(message.channel, sh.mention(message) + ret)

c_kurwa.command = r"(kurwa|fucking|jeban(y|ym|ymi|i|ą|ych)|pierdol(ony|ona|eni|onych|onymi))"
c_kurwa.params = ["zdanie"]
c_kurwa.desc = "Okrasz wypowiedź wyrafinowanym słownictwem!"


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


# -------------------------------------
# obrazki
# -------------------------------------


@asyncio.coroutine
def c_pozdro(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/pzdr.jpg"))

c_pozdro.command = r"(pozdro|pzdr)"
c_pozdro.desc = "pzdr i z fartem"


@asyncio.coroutine
def c_several(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/politbiuro_intensifies.gif"))

c_several.command = r"(several|spat)"
c_several.desc = "Several people are typing..."


@asyncio.coroutine
def c_wiplerine(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/xavier-mikke.jpg"))

c_wiplerine.command = r"(w|v)iplerine"


@asyncio.coroutine
def c_cogif(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/comment_jblSpYCkKHo8hIGeGqLq0xWLjNjfM19j.gif"))

c_cogif.command = r"(co|what)"


@asyncio.coroutine
def c_wypierdalaj(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/comment_yJaXUY8ayZxkMA8s0oLMjNkdj6ajeDLD.gif"))

c_wypierdalaj.command = r"wypierdalaj"


@asyncio.coroutine
def c_wincyj(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/comment_302bIOuE74Qs2AzCr7pjcFmMfGRZvdgn.gif"))

c_wincyj.command = r"wincyj"


@asyncio.coroutine
def c_bkc(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/bk z kg chb z cb.jpg"))

c_bkc.command = r"bkc"


@asyncio.coroutine
def c_zgadzam(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/nargogh wins.png"))

c_zgadzam.command = r"zgadzam"
c_zgadzam.desc = "Się zgadzam z Nargogiem"


# -------------------------------------
# funkcje używające seed
# -------------------------------------


@asyncio.coroutine
def c_czy(client, message):
    yield from client.send_message(message.channel, sh.mention(message) + random.choice(["tak", "nie", "nie wiem", "być może", "na pewno", "to mało prawdopodobne", "nie sądzę", "jeszcze się pytasz?", "tak (żartuję hehe)", "hehe))))))))))))))))))", "tak", "nie", "tak (no homo)", "zaiste", "no chyba cię pambuk opuścił", "raczej nie", "jeszcze nie", "teraz już tak", "może kiedyś", "tak jest panie kapitanie", "panie januszu NIE", "jeszcze nie wiem", "daj mi chwilę to się zastanowię", "nie wiem zarobiony jestem przyjdź Pan jutro", "a czy papież sra w lesie?", "co za debil wymyśla te pytania", "jak najbardziej", "gówno prawda", "jeszcze jak", "jest możliwe", "otóż nie"]))

c_czy.command = r"czy"
c_czy.params = ["zapytanie"]

@asyncio.coroutine
def c_ile(client, message):
    zeros = random.randint(1,4)
    yield from client.send_message(message.channel, sh.mention(message) + str(random.randint(pow(10, zeros-1), pow(10, zeros))))

c_ile.command = r"ile"
c_ile.params = ["zapytanie"]

@asyncio.coroutine
def c_ocen(client, message):
	ocena = random.randint(1, 10)
	doda = ""
	znak = ""
	if ocena < 10 and ocena > 0:
		doda = random.choice(["", ",5", "-", "+"])
	if ocena > 7:
		znak = random.choice(["", "+ <:znak:400312259328606214>", "- Berlin poleca", ""])
	
	yield from client.send_message(message.channel, sh.mention(message) + str(ocena) + doda + "/10 " + znak)

c_ocen.command = r"(ocen|oceń)"
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
	suffix = ["Turambara", "yojca", "Lorda Nargogha", "Rankina", "Kathai", "Behemorta", "orgieła", "Stillborna", "Metalusa", "kicka", "podbiela", "Sedinusa", "Hakkena", "Tebega", "Sermacieja", "t3trisa", "optiego", "Hrabuli", "FaceDancera", "Holiego.Deatha", "Ramzesa", "POLIPa", "mateusza(stefana)", "Xysia", "Germanotty", "Berlina", "8azyliszka", "Seekera", "Murezora", "RIPa", "Aidena", "Accouna", "Fela", "Dracii", "Niziołki", "Mavericka", "P_aula", "Brylanta", "deffika", "Deviusa", "Gofra", "JamesaVooa", "Black Shadowa", "emqiego", "nerv4", "Pałkera", "Princess Nua", "Rysi", "Shakera", "Artiusa", "Stefana", "Xerbera", "gena", "b3rta", "u optiego", "na wydziale elektrycznym", "w Kathowicach", "u Kath w piwnicy", "we Wrocławiu", "w Szczecinie", "w Brwinowie", "w Warszawie", "w Bogatyni", "w Golubiu-Dobrzynie", "w Rzeszowie", "w Krakowie", "w Bydgoszczy", "w Magdalence przy stole z pozostałymi zdrajcami", "tam gdzie stało ZOMO", "na serwerze Interii", "w Gołodupczynie", "w kinie w Berlinie"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(prefix) + " " + random.choice(suffix))

c_gdzie.command = r"gdzie"
c_gdzie.params = ["zapytanie"]

@asyncio.coroutine
def c_kim(client, message):
	word = ["mną", "tobą", "nikim", "Turambarem", "yojecem", "Lordem Nargoghiem", "Rankinem", "Kathajcem", "Behemortem", "orgiełem", "Stillbornem", "Metalusem", "kickiem", "podbielem", "Sedinusem", "Hakkenem", "Tebem", "Sermaciejem", "t3trisem", "optim", "Hrabulą", "FaceDancerem", "Holim.Death", "Ramzesem", "POLIPem", "mateuszem(stefanem)", "Xysiem", "Germanottą", "Berlinem", "8azyliszkiem", "Seekerem", "Murezorem", "RIPem", "Aidenem", "Accounem", "Felem", "Dracią", "Niziołką", "Maverickiem", "P_aulem", "Brylantem", "deffikiem", "Deviusem", "Gofrem", "JamesemVooem", "Black Shadowem", "emqim", "nerv3m", "Pałkerem", "PrincessNuem", "Rysią", "Shakerem", "Artiusem", "Xerberem", "Elanem", "Vodą", "Xardasem", "Abyssem", "Bethezerem", "Knight Martiusem", "Mysquffem", "OATem", "Noobirusem", "Osłem", "b3rtem", "genem", "Śćasem"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(word))

c_kim.command = r"kim"
c_kim.params = ["zapytanie"]

@asyncio.coroutine
def c_kto(client, message):
	word = ["ja", "ty", "nikt", "Turambar", "yojec", "Lord Nargogh", "Rankin", "Kath", "Behemort", "orgiełe", "Stillborn", "Metalus", "kicek", "podbiel", "Sedinus", "Hakken", "Teb", "Sermaciej", "t3tris", "opti", "Hrabula", "FaceDancer", "Holy.Death", "Ramzes", "POLIP", "mateusz(stefan)", "Xysiu", "Germanotta", "Berlin", "8azyliszek", "Seeker", "Murezor", "RIP", "Aiden", "Accoun", "Fel", "Dracia", "Niziołka", "Maverick", "P_aul", "Brylant", "deffik", "Devius", "Gofer", "JamesVoo", "Black Shadow", "emqi", "nerv0", "Pałker", "PrincessNue", "Rysia", "Shaker", "Artius", "Xerber", "Elano", "Voda", "Xardas", "Abyss", "Bethezer", "Knight Martius", "Mysquff", "OAT", "Noobirus", "Osioł", "b3rt", "gen", "Śćas"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(word))

c_kto.command = r"kto"
c_kto.params = ["zapytanie"]

@asyncio.coroutine
def c_kogo(client, message):
	cmd = sh.get_command(message)
	if cmd == ".kogo":
		hrabul = "Hrabulę"
		ja = "mnie"
		ty = "ciebie"
		nikt = "nikogo"
	else:
		hrabul = "Hrabuli"
		if cmd == ".czyim":
			ja = "moim"
			ty = "twoim"
			nikt = "niczyim"
		elif cmd == ".czyja":
			ja = "moja"
			ty = "twoja"
			nikt = "niczyja"
		elif cmd == ".czyje":
			ja = "moje"
			ty = "twoje"
			nikt = "niczyje"
		elif cmd == ".czyj":
			ja = "mój"
			ty = "twój"
			nikt = "niczyj"
	
	word = [ja, ty, "Turambara", "yojca", "Lorda Nargogha", "Rankina", "Kathajca", "Behemorta", "orgieła", "Stillborna", "Metalusa", "kicka", "podbiela", "Sedinusa", "Hakkena", "Teba", "Sermacieja", "t3trisa", "optiego", hrabul, "FaceDancera", "Holiego.Deatha", "Ramzesa", "POLIPa", "mateusza(stefana)", "Xysia", "Germanotty", "Berlina", "8azyliszka", "Seekera", "Murezora", "RIPa", "Aidena", " Accouna", "Fela", "Dracii", "Niziołki", "Mavericka", "P_aula", "Brylanta", "deffika", "Deviusa", "Gofra", "JamesaVooa", "Black Shadowa", "emqiego", "nerv4", "Pałkera", "PrincessNua", "Rysi", "Shakera", "Artiusa", "Stefana", "Xerbera", "Elana", "Vodę", "Xardasa", "Abyssa", "Bethezera", "Knight Martiusa", "Mysquffa", "OATa", "Noobirusa", "Osła", "b3rta", "gena", "Śćasa"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(word))

c_kogo.command = r"(kogo|czyim|czyj(a|e)?)"
c_kogo.params = ["zapytanie"]

@asyncio.coroutine
def c_komu(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(["mi", "tobie", "nikomu", "Turambarowi", "yojcu", "Lordowi Nargoghowi", "Rankinowi", "Kathajce", "Behemortowi", "orgiełowi", "Stillbornowi", "Metalusowi", "kickowi", "podbielowi", "Sedinusowi", "Hakkenowi", "Tebegowi", "Sermaciejowi", "t3trisowi", "optiemu", "Hrabuli", "FaceDancerowi", "Holiemu.Deathowi", "lghostowi", "POLIPowi", "mateuszowi(stefanowi)", "Xysiowi", "Germanotcie", "Berlinowi", "8azyliszkowi", "Seekerowi", "Murezorowi", "R1Powi", "Aidenowi", "Trepliev", "Accounowi", "Śćasowi"]))

c_komu.command = r"komu"
c_komu.params = ["zapytanie"]


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
	yield from client.send_message(message.channel, "yeah, I see that")

f_iseethat.command = r'specially since (it(\')?s|theyre|they\'re) such good size'
f_iseethat.prob = 1.0

@asyncio.coroutine
def f_goodadvice(client, message):
	yield from client.send_message(message.channel, "daddy gave you good advice")
	
f_goodadvice.command = r'^yea(h)?(,)? i see that'
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

f_iriptheskin.command = r'^[mh]{12,}'
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
f_cogowno.prob = 0.05

@asyncio.coroutine
def f_czyzby(client, message):
	yield from client.send_message(message.channel, "chyba ty")

f_czyzby.command = r'(czyzby|czyżby)'
f_czyzby.prob = 0.25

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
f_rucha.prob = 0.05

@asyncio.coroutine
def f_wulg(client, message):
	yield from client.send_message(message.channel, random.choice(["może byś tak kurwa nie przeklinał", "co?", "bez wulgaryzmów proszę", "na ten kanał zaglądają dzieci", "ostrożniej z językiem", "to kanał PG13", "czy mam ci język uciąć?", "przestań przeklinać pedale bo cię stąd wypierdolę dyscyplinarnie", "pambuk płacze jak przeklinasz", "mów do mnie brzydko", "Kath bączy jak przeklinasz", "proszę tu nie przeklinać, to porządna knajpa", "nie ma takiego przeklinania chuju", "блять))))))))))", "zamknij pizdę"]))

f_wulg.command = r'(kurw|chuj|pierdol|pierdal|jeb)'
f_wulg.prob = 0.05

@asyncio.coroutine
def f_witam(client, message):
	yield from client.send_message(message.channel, random.choice(["witam na kanale i życzę miłej zabawy", "cześć, kopę lat", "siemanko witam na moim kanale", "witam witam również", "no elo", "salam alejkum", "привет", "dzińdybry", "siemaszki", "serwus", "gitara siema", "dobrý den", "pozdrawiam, Mariusz " + random.choice(["Gambal", "Handzlik"]), "feedlysiemka " + str(message.author).split("#")[0].lower() + "ox"]))

f_witam.command = r'(witam|cześć|czesc|siema|szalom|joł|shalom|dzi(n|ń)dybry|dzie(n|ń) dobry|siemka)'
f_witam.prob = 0.5

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
	replies = ["USUŃ TO", "boga w sercu nie masz?", "jezus maria...", "całe życie z debilami", "a bana to byś nie chciał?", "<rzygi>", "ty bamboclu"]
	
	if random.random() < 1/(len(replies)+1):
		yield from client.send_typing(message.channel)
		yield from c_wypierdalaj(client, message)
	else:
		yield from client.send_message(message.channel,  random.choice(replies))

f_jakisgolas.command = r"vkPCjJM.jpg"
f_jakisgolas.prob = 1.0


#@asyncio.coroutine
#def f_nawzajem(client, message):
#	yield from client.send_message(message.channel, "nawzajem")

#f_nawzajem.command = r"weso(l|ł)"
#f_nawzajem.prob = 1.0


# -------------------------------------
# rzut koscia
# -------------------------------------


@asyncio.coroutine
def c_dice(client, message):
	""".dice <formula> - Rolls dice using the XdY format, also does basic (+-*/) math."""
	#MATHTIME! Let's prepare the failsafes.
	legal_formula, no_dice = 1, 1
	#parsing time.
	msg = sh.get_args(message)
	formula = msg #back-up the original message, because you're going to feed it back to the user in the end.
	formula = formula.replace("-", " - ")
	formula = formula.replace("+", " + ") #add spaces
	formula = formula.replace("/", " / ") #for all
	formula = formula.replace("*", " * ") #the characters
	formula = formula.replace("(", " ( ") #supported
	formula = formula. replace(")", " ) ")
	arr = formula.split(" ") #aaaand, CUT IT APART! (this is why you needed the spaces.)
	full_string = "" #reset the formula
	for segment in arr:
		#let's look at this formula... piece, by, piece
		if segment != "":
			#the value of this segment is 0
			value = 0
			if re.search("[0-9]*(d|D|k|K)[0-9]+", segment): #if there's a dice (regex FTW!)
				value = rollDice(segment.lower()) #then roll the dice.
				no_dice = 0 # And let the bot know there's dice in the formula
			elif re.search("([0-9]|\+|\-|\*|\/|\(|\)| \+| \-| \*| \/| \(| \))", segment): #are any of the supported math characters in this piece?
				value = segment #then just make that the value.
			else:
				legal_formula = 0 #non-supported character found...
				break #ABORT, ABORT, ABORT!
			full_string += value #add this segment's value to the full string
	#repeat next segment
	#you done? good.
	if legal_formula == 1 and full_string != "": # did something break? no? good, continue.
		#at this point full string is something like: "4 + 6 + 12 * 4" etc.
		result = str(eval(full_string)) # so normally eval is UNSAFE... but since i've dumped regex over the user input i'm pretty confident in the security.
		#print result to chat
		if(no_dice): #no dice found, warn!
			yield from client.send_message(message.channel, sh.mention(message) + msg+" = "+result)
		else: #dice found, just let the users know what's happening
			yield from client.send_message(message.channel, sh.mention(message) + "wyrzucono "+msg+" ("+full_string+"): "+result)
	else: #print illegal warning.
		yield from client.send_message(message.channel, sh.mention(message) + "coś tu jest nie teges: "+segment)

c_dice.command = r"(d|dice|roll|rzut|rzuc)"
c_dice.params = ["XdY / XkY"]
c_dice.desc = "Rzut kością"

def rollDice(diceroll):
#Time for the real fun, dice!
	if "k" in diceroll.lower():
		delimiter = "k"
	else:
		delimiter = "d"
	
	if(diceroll.lower().startswith(delimiter)): #check if it's XdX or dX
		#  dX
		rolls = 1 #no dice amounts specified, roll 1
		size = int(diceroll[1:]) # dice with this amount of sides
	else:
		# XdX
		rolls = int(diceroll.lower().split(delimiter)[0]) # dice amount specified, use it.
		size = int(diceroll.lower().split(delimiter)[1]) #  aswell as this size.
	result = "" #dice result is zero.
	for i in range(1,rolls+1): #for the amount of dice
		#roll 10 dice, pick a random dice to use, add string to result.
		# I should elaborate on this...
		# str() makes sure the number is in string format (required for the eval())
		# random.randint(1,size) is 1 dice and random.randint(0,9) selects one of the ten dice rolled
		# reason for this is fairness, true random has at least 2 stages.
		result += str((random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size))[random.randint(0,9)])
		if(i != rolls):
			#if it's not the last sign, add a plus sign.
			result += "+"
	return "("+result+")" #feed it back to the formula parser... add some parentheses so we know this is 1 roll.


# -------------------------------------
# do wykonania o określonych godzinach
# -------------------------------------


@asyncio.coroutine
def t_pope_time(client, channels):
	choices = ["zapraszam wszystkich na kremówki", "wybiła godzina papieska", "Jan Paweł 2, w moim sercu zawsze 1", "Jan Paweł II był wielkim człowiekiem", "JP2GMD"]
	barka = ("Pan kiedyś stanął nad brzegiem,\n" +
		"Szukał ludzi gotowych pójść za Nim;\n" +
		"By łowić serca\n" +
		"Słów Bożych prawdą.\n\n" +
		"Ref.: \n" +
		"O Panie, to Ty na mnie spojrzałeś,\n" +
		"Twoje usta dziś wyrzekły me imię.\n" +
		"Swoją barkę pozostawiam na brzegu,\n" +
		"Razem z Tobą nowy zacznę dziś łów.")
	
	reply = random.choice([random.choice(choices), barka])
	
	for ch in channels:
		yield from client.send_message(ch, reply)

t_pope_time.channels = ["174449535811190785"]
t_pope_time.time = "21:37"


@asyncio.coroutine
def t_trzytrzytrzy(client, channels):
	choices = ["3:33, KATH POBUDKA"]
	
	reply = random.choice(choices)
	
	for ch in channels:
		yield from client.send_message(ch, reply)

t_trzytrzytrzy.channels = ["174449535811190785"]
t_trzytrzytrzy.time = "3:33"


#@asyncio.coroutine
#def t_test(client, channels):
#	yield from client.send_message(channels[0], "test")
#
#t_test.channels = ["174449535811190785"]
#t_test.time = "16:25"