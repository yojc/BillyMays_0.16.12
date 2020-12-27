import random
import asyncio
import time
import re
from discord.utils import find

import billy_shared as sh

from _MemePy import MemeGenerator

def get_avatar_url(client, message, nickname_raw=None):
	nickname = nickname_raw or sh.get_args(message) or message.author.name
	user_array = message.server.members if message.server else client.get_all_members()
	
	ret = find(lambda m: re.search(nickname, m.display_name, flags=re.I), user_array)

	if not ret:
		ret = find(lambda m: re.search(nickname, m.name, flags=re.I), user_array)
	
	if ret:
		return (ret.avatar_url or ret.default_avatar_url)
	else:
		return None

def get_emoji_url(client, message, emoname_raw=None):
	emoname = emoname_raw or sh.get_args(message) or ""

	ret = None

	def get_emoji(name, array):
		if name.isnumeric() and len(name) > 5:
			return find(lambda e: re.search(emoname, e.id, flags=re.I), array)
		elif re.match(r"<a?:\S+:\d+>", name):
			anim_flag = "a" if name.startswith("<a:") else ""
			return find(lambda e: re.search(emoname, "<" + anim_flag + ":" + e.name + ":" + e.id + ">", flags=re.I), array)
		else:
			return find(lambda e: re.search(emoname, e.name, flags=re.I), array)

	if message.server:
		ret = get_emoji(emoname, message.server.emojis)
	
	if not ret:
		ret = get_emoji(emoname, client.get_all_emojis())
	
	if ret:
		return (ret.url + "?v=1").replace("discordapp", "cdn.discordapp").replace("/api/", "/")
	else:
		return None


# ----------------- #

@asyncio.coroutine
def c_memegenerator(client, message):
	args = sh.get_args(message)
	tmp = args.split(" ")

	if len(args) == 0 or len(args.split(" ")) == 1:
		yield from client.send_message(message.channel, sh.mention(message) + "chyba coś źle wpisał{}ś, poprawna składnia: `.meme nazwa tekst 1; tekst 2; itd.`".format("a" if sh.is_female(message) else "e"))
	else:
		meme_name = tmp[0].strip()
		meme_labels = [label.strip() for label in args[len(meme_name)+1:].split(";")]

		for i, label in enumerate(meme_labels):
			try:
			# Check if emoji
				if re.match(r"^emo(ji)?:", label):
					meme_labels[i] = "<" + get_emoji_url(client, message, label[label.index(":")+1:].strip(" ")) + ">"
				elif re.match(r"<a?:\S+:\d+>", label):
					meme_labels[i] = "<" + get_emoji_url(client, message, label) + ">"
				# Check if avatar
				elif re.match(r"^av(atar)?:", label):
					meme_labels[i] = "<" + get_avatar_url(client, message, label[label.index(":")+1:].strip(" ")) + ">"
			except TypeError:
				yield from client.send_message(message.channel, "Nie znaleziono avatara/emoji")
				return

		meme_filename = time.strftime("meme_%Y-%m-%d_%H-%M-%S.png")

		try:
			meme_image_bytes = MemeGenerator.get_meme_image_bytes(meme_name, meme_labels)
			yield from client.send_file(message.channel, meme_image_bytes, filename=meme_filename)
		except Exception as e:
			yield from client.send_message(message.channel, "Coś tu jest nie teges. (`{}`)".format(str(e)))

c_memegenerator.command = r"meme?"
c_memegenerator.params = ["nazwa", "tekst 1;", "tekst 2;", "itd."]
c_memegenerator.desc = "Generator memów"



@asyncio.coroutine
def c_get_avatar_url(client, message):
	nickname = sh.get_args(message) or message.author.name
	
	av = get_avatar_url(client, message)

	if av:
		yield from client.send_message(message.channel, av)
	else:
		yield from client.send_message(message.channel, "Nie znaleziono")

c_get_avatar_url.command = r"(av|avatar)"

@asyncio.coroutine
def c_get_emoji_url(client, message):
	emo = get_emoji_url(client, message)

	if emo:
		yield from client.send_message(message.channel, emo)
	else:
		yield from client.send_message(message.channel, "Nie znaleziono")

c_get_emoji_url.command = r"(emo|ji)"