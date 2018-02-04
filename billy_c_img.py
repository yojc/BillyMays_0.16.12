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


@asyncio.coroutine
def c_wish(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/THATSME.jpg"))

c_wish.command = r"wish"
c_wish.desc = "god I wish it was me"


@asyncio.coroutine
def c_babe(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/marian_czy_ty_mnie_kochasz.jpg"))

c_babe.command = r"(chlopprzebranyza)?babe"

@asyncio.coroutine
def c_smaglor(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/lanbajlan.png"))

c_smaglor.command = r"(komarcz|smaglor)"

@asyncio.coroutine
def c_zzz(client, message):
	yield from client.send_file(message.channel, sh.file_path("img/zzz.gif"))

c_zzz.command = r"zzz"