import asyncio
import random

import billy_shared as sh
import billy_rhymes as rhymes

# -------------------------------------
# rymy
# -------------------------------------

@asyncio.coroutine
def c_accounie(client, message):
	rhyme = rhymes.unie
	ret = "Accounie Accounie ty"
	custom = ["ślunski pierunie", "ajfonie", "żydomasonie"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_accounie.command = r"accounie"
c_accounie.rhyme = True


@asyncio.coroutine
def c_aiden(client, message):
	rhyme = rhymes.en
	ret = "Aiden"
	custom = ["rudy aborygen"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_aiden.command = r"aiden"
c_aiden.rhyme = True


@asyncio.coroutine
def c_behemort(client, message):
	rhyme = rhymes.ort
	ret = "Behemort"
	custom = ["zjada małe dzieci"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_behemort.command = r"behemort"
c_behemort.rhyme = True


@asyncio.coroutine
def c_brylu(client, message):
	rhyme = rhymes.ylu
	ret = "Brylu Brylu ty"
	custom = ["bezglutenowy chasydzie", "debilu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_brylu.command = r"brylu"
c_brylu.rhyme = True


@asyncio.coroutine
def c_deffiku(client, message):
	rhyme = rhymes.iku
	ret = "deffiku deffiku ty"
	custom = ["mamuci siku"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_deffiku.command = r"deffiku"
c_deffiku.rhyme = True


@asyncio.coroutine
def c_felu(client, message):
	rhyme = rhymes.elu
	ret = "felu felu ty"
	custom = ["taki fajniejszy podbielu", "niemiecki nieprzyjacielu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_felu.command = r"felu"
c_felu.rhyme = True


@asyncio.coroutine
def c_gen(client, message):
	rhyme = rhymes.en
	ret = "gen"
	custom = ["homoseksualny aborygen"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_gen.command = r"gen"
c_gen.rhyme = True


@asyncio.coroutine
def c_goferze(client, message):
	rhyme = rhymes.erze
	ret = "Goferze Goferze ty"
	custom = ["krowi placku z bitą śmietaną i ekstra dużymi kawałkami owoców"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_goferze.command = r"goferze"
c_goferze.rhyme = True


@asyncio.coroutine
def c_kathai(client, message):
	rhyme = rhymes.ai
	ret = "Kathai"
	custom = ["uahai dicki dwai", "s-senpai"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_kathai.command = r"kath?a(i|j)"
c_kathai.rhyme = True


@asyncio.coroutine
def c_kathajec(client, message):
	rhyme = rhymes.jec
	ret = "Kathajec"
	custom = ["bez jajec"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_kathajec.command = r"(kathajec|katajec)"
c_kathajec.rhyme = True


@asyncio.coroutine
def c_kicku(client, message):
	rhyme = rhymes.icku
	ret = "kicku kicku"
	custom = ["ty mały dicku", "thiccku"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_kicku.command = r"kicku"
c_kicku.rhyme = True


@asyncio.coroutine
def c_lghoscie(client, message):
	rhyme = rhymes.oscie
	ret = "LaserGhoście ty"
	custom = ["amigowca wal z gumowca"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_lghoscie.command = r"lghoscie"
c_lghoscie.rhyme = True


@asyncio.coroutine
def c_nargogu(client, message):
	rhyme = rhymes.ogu
	ret = "Nargogu Nargogu ty"
	custom = ["mentalny kucu", "niemyty pierogu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_nargogu.command = r"nargogh?u"
c_nargogu.rhyme = True


@asyncio.coroutine
def c_orgu(client, message):
	rhyme = rhymes.rgu
	ret = "orgu orgu ty"
	custom = ["cybochuju", "ruski czołgu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_orgu.command = r"orgu"
c_orgu.rhyme = True


@asyncio.coroutine
def c_pewkerze(client, message):
	rhyme = rhymes.erze
	ret = "Pewkerze Pewkerze ty"
	custom = ["lamerze"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_pewkerze.command = r"(pewkerze|palkerze|pałkerze)"
c_pewkerze.rhyme = True


@asyncio.coroutine
def c_podbielu(client, message):
	rhyme = rhymes.elu
	ret = "podbielu podbielu ty"
	custom = ["łysy cwelu", "analny skurwielu", "odbyta niszczycielu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_podbielu.command = r"podbielu"
c_podbielu.rhyme = True


@asyncio.coroutine
def c_polipie(client, message):
	rhyme = rhymes.ipie
	ret = "POLIPie POLIPie ty"
	custom = ["glucie z nosa", "najserdeczniejszy przyjacielu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_polipie.command = r"polipie"
c_polipie.rhyme = True


@asyncio.coroutine
def c_srane(client, message):
	rhyme = rhymes.rane
	ret = "rane rane"
	custom = ["pojebane", "witane witane", "w letspleju nagrane", "na jutubie obejrzane"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_srane.command = r"srane"
c_srane.rhyme = True


@asyncio.coroutine
def c_rysiu(client, message):
	rhyme = rhymes.ysiu_isiu
	ret = "Rysiu Rysiu ty"
	custom = ["zwierzaku", "kiedyś miałaś lepszy brzuch", "bestio z Wadowic"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_rysiu.command = r"rysiu"
c_rysiu.rhyme = True


@asyncio.coroutine
def c_seekerze(client, message):
	rhyme = rhymes.erze
	ret = "Seekerze Seekerze ty"
	custom = ["przestań mnie dotykać w nocy", "najlepszy przyjacielu R1Pa", "lubisz macierze", "białoruski drwalu"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_seekerze.command = r"seekerze"
c_seekerze.rhyme = True


@asyncio.coroutine
def c_sermacieju(client, message):
	rhyme = rhymes.eju
	ret = "Sermacieju ty"
	custom = ["radości z życia złodzieju", "jebaku leśny"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_sermacieju.command = r"sermacieju"
c_sermacieju.rhyme = True


@asyncio.coroutine
def c_tebie(client, message):
	rhyme = rhymes.ebie
	ret = "Tebie ty"
	custom = ["kurwo jerychońska"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_tebie.command = r"tebie"
c_tebie.rhyme = True


@asyncio.coroutine
def c_tet(client, message):
	rhyme = rhymes.det_tet
	ret = "t3t"
	custom = ["naplet", "ty chuju"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_tet.command = r"(tet|t3t)"
c_tet.rhyme = True


@asyncio.coroutine
def c_tetrisie(client, message):
	rhyme = rhymes.isie
	ret = "t3trisie ty"
	custom = ["afrożydowska kurwo"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_tetrisie.command = r"(tet|t3t)risie"
c_tetrisie.rhyme = True


@asyncio.coroutine
def c_tetrzycie(client, message):
	rhyme = rhymes.ycie
	ret = "t3trzycie t3trzycie ty"
	custom = ["kapitanie mokrybąk"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_tetrzycie.command = r"(tet|t3t)rzycie"
c_tetrzycie.rhyme = True


@asyncio.coroutine
def c_trepli(client, message):
	rhyme = rhymes.pli
	ret = "Trepli"
	custom = ["jest gorsza od Kath bo ma tylko jednego dicka"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_trepli.command = r"trepli"
c_trepli.rhyme = True


@asyncio.coroutine
def c_turq(client, message):
	rhyme = rhymes.urku
	ret = "Turq Turq ty"
	custom = ["robotny fiucie"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_turq.command = r"turq"
c_turq.rhyme = True


@asyncio.coroutine
def c_xysiu(client, message):
	rhyme = rhymes.ysiu_isiu
	ret = "Xysiu Xysiu ty"
	custom = ["żydowski rabinie"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_xysiu.command = r"xysiu"
c_xysiu.rhyme = True


@asyncio.coroutine
def c_yojec(client, message):
	rhyme = rhymes.jec
	ret = "yojec"
	custom = ["srojec", "cyklotron"]
	yield from client.send_message(message.channel, ret + rhymes.compose(rhyme, custom))

c_yojec.command = r"yojec"
c_yojec.rhyme = True


# -------------------------------------
# jakies inne bzdety
# -------------------------------------


@asyncio.coroutine
def c_behe(client, message):
	ret = 'Be'
	for x in range(0, random.randint(1, 15)):
		ret += 'he'
	yield from client.send_message(message.channel, ret+'mort')

c_behe.command = r"behe"
c_behe.desc = "Behehemort"
c_behe.rhyme = True

@asyncio.coroutine
def c_hakken(client, message):
	ret = 'Ha'
	for x in range(0, random.randint(0, 14)):
		ret += 'ha'
	yield from client.send_message(message.channel, ret+'kken')

c_hakken.command = r"hakken"
c_hakken.desc = "Hahahakken"
c_hakken.rhyme = True


@asyncio.coroutine
def c_kath(client, message):
	ret = 'Ka'
	for x in range(0, random.randint(0, 14)):
		ret += 'ka'
	ret += "thai_Na"
	for x in range(0, random.randint(0, 14)):
		ret += 'na'
	yield from client.send_message(message.channel, ret+'njika')

c_kath.command = r"kath"
c_kath.desc = "Kakakathai"
c_kath.rhyme = True


@asyncio.coroutine
def c_kicek(client, message):
	yield from client.send_message(message.channel, random.choice(["kicek", "kiceg"]) + " mały " + random.choice(["bicek", "dicek", "cycek"]))

c_kicek.command = r"kicek"
c_kicek.desc = "kicek mały..."
c_kicek.rhyme = True


@asyncio.coroutine
def c_nargog(client, message):
	ret = 'Na'
	for x in range(0, random.randint(0, 14)):
		ret += 'na'
	yield from client.send_message(message.channel, ret+'rgogh')

c_nargog.command = r"nargog(h)?"
c_nargog.desc = "Nananargogh"
c_nargog.rhyme = True


@asyncio.coroutine
def c_polip(client, message):
	ret = 'POLI'
	for x in range(0, random.randint(0, 14)):
		ret += 'POLI'
	yield from client.send_message(message.channel, ret + random.choice(["P", "POLIK"]))

c_polip.command = r"polip"
c_polip.desc = "POLIPOLIPOLIK"
c_polip.rhyme = True


@asyncio.coroutine
def c_rane(client, message):
	ret = "Ra"
	for x in range(0, 14):
		if random.randint(0, 1) == 1:
			ret += 'ra'
		else:
			ret += "ne"
	yield from client.send_message(message.channel, ret)

c_rane.command = r"rane"
c_rane.desc = "raranene"
c_rane.rhyme = True


@asyncio.coroutine
def c_teb(client, message):
	ret = 'Teb'
	for x in range(0, random.randint(0, 14)):
		ret += 'eb'
	yield from client.send_message(message.channel, ret + "eg")

c_teb.command = r"teb"
c_teb.desc = "Tebebeg"
c_teb.rhyme = True


@asyncio.coroutine
def c_tebeg(client, message):
	yield from client.send_message(message.channel, "T E B E G\nE\nB\nE\nG")

c_tebeg.command = r"tebeg"
c_tebeg.desc = "T E B E G"
c_tebeg.rhyme = True


@asyncio.coroutine
def c_yojc(client, message):
	count = random.randint(0, 14)
	flag = random.randint(0, 1)
	
	if count < 2:
		where = 0
	else:
		where = random.randint(1, count-1)
	
	ret = "yo"
	
	for x in range(0, count):
		ret += 'yo'
		if flag == 1 and x == where:
			ret += "motherfucker"
	
	yield from client.send_message(message.channel, ret+'jc')

c_yojc.command = r"yojc"
c_yojc.desc = "yoyoyojc"
c_yojc.rhyme = True
