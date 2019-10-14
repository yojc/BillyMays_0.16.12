import random
import asyncio

import billy_shared as sh


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

c_cogif.command = r"(co|czo|what)"


@asyncio.coroutine
def c_wypierdalaj(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/comment_yJaXUY8ayZxkMA8s0oLMjNkdj6ajeDLD.gif"))

c_wypierdalaj.desc = "hidden"
#c_wypierdalaj.command = r"wypierdalaj"


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
	if random.random() < 0.1:
		yield from client.send_file(message.channel, sh.file_path("img/dracia_intensifies.gif"))
	else:
		yield from client.send_file(message.channel, sh.file_path("img/nargogh wins.png"))

c_zgadzam.command = r"zgadzam"
c_zgadzam.desc = "Się zgadzam z Nargogiem"


@asyncio.coroutine
def c_wish(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/THATSME.jpg"))

c_wish.command = r"wish"
c_wish.desc = "god I wish it was me"


@asyncio.coroutine
def c_babe(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/marian_czy_ty_mnie_kochasz.jpg"))

c_babe.command = r"(chlopprzebranyza)?bab(a|e)"

@asyncio.coroutine
def c_smaglor(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/lanbajlan.png"))

c_smaglor.command = r"(komarcz|smaglor)"

@asyncio.coroutine
def c_zzz(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/zzz.gif"))

c_zzz.command = r"zzz"

@asyncio.coroutine
def c_dojce(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/parampampam.jpg"))

c_dojce.command = r"dojce"

@asyncio.coroutine
def c_cisza(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/SILENCE OR I WILL KILL YOU.jpg"))

c_cisza.command = r"(cisza|silence)"


@asyncio.coroutine
def c_afera(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/comment_5DTDRHYuWYyVyTXzQGs7SvHZtyDz2sF8.gif"))

c_afera.command = r"afera"


@asyncio.coroutine
def c_vnag(client, message):
	if random.random() < 0.1:
		yield from client.send_file(message.channel, sh.file_path("img/bruk-teb mountain.png"))
	else:
		yield from client.send_file(message.channel, sh.file_path("img/teb.png"))

c_vnag.command = r"(nice|very(nice(and(gay)?)?)?|vnag)"


@asyncio.coroutine
def c_okazja(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/to_sie_nazywa_antycypowanie_norek.png"))

c_okazja.command = r"okazja"


@asyncio.coroutine
def c_dupie(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/ASS.png"))

c_dupie.command = r"(dupa|dupie)"


@asyncio.coroutine
def c_dupe(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/your face your ass whats the difference.png"))

c_dupe.command = r"(dupe)"


@asyncio.coroutine
def c_ociehuj(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/nasralem.jpg"))

c_ociehuj.command = r"ociec?huj"


@asyncio.coroutine
def c_zrozumiale(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/zrozumiale.webm"))

c_zrozumiale.command = r"(zrozumialem?|understandable|understood)"


@asyncio.coroutine
def c_provocative(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/provo.mp4"))

c_provocative.command = r"(provo(cative)?|prowo)"


@asyncio.coroutine
def c_nasralem(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/magiczny_napoj_metalusa.jpg"))

c_nasralem.command = r"(nasra(l|ł)em)"


@asyncio.coroutine
def c_uwal(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/hej kup se klej.jpg"))

c_uwal.command = r"(uwal|pizde|pizdę)"


@asyncio.coroutine
def c_silversurfer(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/zal.pl.png"))

c_silversurfer.command = r"(silversurfer|ss|rzal|zal)"


@asyncio.coroutine
def c_nawzajem(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/nawzajem.jpg"))

c_nawzajem.command = r"nawzajem"


@asyncio.coroutine
def c_stop(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/ELMO.mp4"))

c_stop.command = r"stop"


@asyncio.coroutine
def c_gofapota(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/gofa_pota.png"))

c_gofapota.command = r"(gofa|pota|gofapota|hari|haripota)"


@asyncio.coroutine
def c_pierdolisz(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/parmezany.jpg"))

c_pierdolisz.command = r"pierdolisz"


@asyncio.coroutine
def c_dzonka(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/still a better love story than meblosciankalight.JPG"))

c_dzonka.command = r"(dt|dzonka|tur)"


@asyncio.coroutine
def c_epic(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/oatw10sekund.webm"))

c_epic.command = r"(oat|epic)"


@asyncio.coroutine
def c_rabin(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/xysiu.webm"))

c_rabin.command = r"(rabin|rabbi)"


@asyncio.coroutine
def c_spierdalaj(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/wuppertal.png"))

c_spierdalaj.command = r"spierdalaj"


@asyncio.coroutine
def c_klasnij(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/rubik.png"))

c_klasnij.command = r"klasnij"


@asyncio.coroutine
def c_lyj(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/rudy_szubert.png"))

c_lyj.command = r"l(e|y)j"


@asyncio.coroutine
def c_mydli(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/mydli.jpg"))

c_mydli.command = r"mydli"


@asyncio.coroutine
def c_dobrze(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/dobrze.webm"))

c_dobrze.command = r"(dobrze|prawda)"


@asyncio.coroutine
def c_zle(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/zle.webm"))

c_zle.command = r"(zle|falsz)"


@asyncio.coroutine
def c_debbie(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/debbie.jpg"))

c_debbie.command = r"(debiru|pierdole)"