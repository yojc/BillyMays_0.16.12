import random
import asyncio
import itertools
import re
import unidecode

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
def c_fullwidth(client, message):
	HALFWIDTH_TO_FULLWIDTH = str.maketrans(
		'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~',
		'０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～')
	
	yield from client.send_message(message.channel, unidecode.unidecode(sh.get_args(message, True)).translate(HALFWIDTH_TO_FULLWIDTH))

c_fullwidth.command = r"fullwidth"


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
		("b", "🅱️"),
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
	nicks = ["Hrabuli", "Turambara", "yojca", "Lorda Nargogha", "Rankina", "Kathajca", "Behemorta", "orgieła", "Stillborna", "Metalusa", "kicka", "podbiela", "Sedinusa", "Hakkena", "Teba", "Sermacieja", "t3trisa", "optiego", "FaceDancera", "Holiego.Deatha", "Ramzesa", "POLIPa", "mateusza(stefana)", "Xysia", "Germanotty", "Berlina", "8azyliszka", "Seekera", "Murezora", "RIPa", "Aidena", " Accouna", "Fela", "Dracii", "Niziołki", "Mavericka", "P_aula", "Brylanta", "deffika", "Deviusa", "Gofra", "JamesaVooa", "Black Shadowa", "emqiego", "nerv4", "Pałkera", "PrincessNua", "Rysi", "Shakera", "Artiusa", "Stefana", "Xerbera", "Elana", "Vodę", "Xardasa", "Abyssa", "Bethezera", "Knight Martiusa", "Mysquffa", "OATa", "Noobirusa", "Osła", "b3rta", "gena", "Śćasa"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(["tak", "nie", "nie wiem", "być może", "na pewno", "to mało prawdopodobne", "nie sądzę", "jeszcze się pytasz?", "tak (żartuję hehe)", "hehe))))))))))))))))))", "tak", "nie", "tak (no homo)", "zaiste", "no chyba cię pambuk opuścił", "raczej nie", "jeszcze nie", "teraz już tak", "może kiedyś", "tak jest panie kapitanie", "panie januszu NIE", "jeszcze nie wiem", "daj mi chwilę to się zastanowię", "nie wiem zarobiony jestem przyjdź Pan jutro", "a czy papież sra w lesie?", "co za debil wymyśla te pytania", "jak najbardziej", "gówno prawda", "jeszcze jak", "jest możliwe", "otóż nie", "nie wiem, spytaj {}".format(random.choice(nicks))]))

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
	
	word = [ja, ty, nikt, "Turambara", "yojca", "Lorda Nargogha", "Rankina", "Kathajca", "Behemorta", "orgieła", "Stillborna", "Metalusa", "kicka", "podbiela", "Sedinusa", "Hakkena", "Teba", "Sermacieja", "t3trisa", "optiego", hrabul, "FaceDancera", "Holiego.Deatha", "Ramzesa", "POLIPa", "mateusza(stefana)", "Xysia", "Germanotty", "Berlina", "8azyliszka", "Seekera", "Murezora", "RIPa", "Aidena", " Accouna", "Fela", "Dracii", "Niziołki", "Mavericka", "P_aula", "Brylanta", "deffika", "Deviusa", "Gofra", "JamesaVooa", "Black Shadowa", "emqiego", "nerv4", "Pałkera", "PrincessNua", "Rysi", "Shakera", "Artiusa", "Stefana", "Xerbera", "Elana", "Vodę", "Xardasa", "Abyssa", "Bethezera", "Knight Martiusa", "Mysquffa", "OATa", "Noobirusa", "Osła", "b3rta", "gena", "Śćasa"]
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(word))

c_kogo.command = r"(kogo|czyi(m|mi|ch)|czyj(a|e|ą)?) "
c_kogo.params = ["zapytanie"]

@asyncio.coroutine
def c_komu(client, message):
	yield from client.send_message(message.channel, sh.mention(message) + random.choice(["mi", "tobie", "nikomu", "Turambarowi", "yojcu", "Lordowi Nargoghowi", "Rankinowi", "Kathajce", "Behemortowi", "orgiełowi", "Stillbornowi", "Metalusowi", "kickowi", "podbielowi", "Sedinusowi", "Hakkenowi", "Tebegowi", "Sermaciejowi", "t3trisowi", "optiemu", "Hrabuli", "FaceDancerowi", "Holiemu.Deathowi", "lghostowi", "POLIPowi", "mateuszowi(stefanowi)", "Xysiowi", "Germanotcie", "Berlinowi", "8azyliszkowi", "Seekerowi", "Murezorowi", "R1Powi", "Aidenowi", "Trepliev", "Accounowi", "Śćasowi"]))

c_komu.command = r"komu"
c_komu.params = ["zapytanie"]