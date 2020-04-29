import discord
import random
import asyncio

import requests
import json
import time

import billy_shared as sh
from config import twitch_key


politbiuro_main_channel = "174449535811190785"
politbiuro_ograch = "639853618568232982"
politbiuro_retro = "305100969191014404"
politbiuro_japabocie = "386148571529084929"

twitch_check_frequency = 5 # minutes
twitch_announcement_cooldown = 19.5 # minutes
twitch_start_time = time.time() - (twitch_announcement_cooldown-twitch_check_frequency)*60

# to find out the user ID
# curl -H "client-id: [twitch-id]" https://api.twitch.tv/helix/users?login=[login]

twitch_streamers = {
	"44844181" : { 
		"nickname" : "yojc", 
		"url" : "https://www.twitch.tv/yojo2", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_retro],
		"mention_group" : "<@&672691296091111424>"
	},

	"237017365" : { 
		"nickname" : "Komstuch", 
		"url" : "https://www.twitch.tv/komstuch", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&674317267198279682>"
	},

	"191881998" : { 
		"nickname" : "Artius", 
		"url" : "https://www.twitch.tv/izdebeth", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&674317361066803210>"
	},

	"51708433" : { 
		"nickname" : "Abyss", 
		"url" : "https://www.twitch.tv/abyss121", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&674317320520466433>"
	},

	"48895107" : { 
		"nickname" : "kiceg", 
		"url" : "https://www.twitch.tv/kicegg", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&693760408615518209>"
	}

	#"40426372" : { 
	#	"nickname" : "Teb", 
	#	"url" : "https://www.twitch.tv/Tebeg", 
	#	"last_seen" : time.time(),
	#	"discord_channels" : [politbiuro_japabocie]
	#}
}


@asyncio.coroutine
def t_twitch_announcements(client, channels):
	global twitch_key
	global twitch_streamers

	sh.print_warning("### TWITCH TEST ### " + time.strftime("%Y-%m-%d %H:%M:%S"))

	headers = {"client-id": twitch_key}
	s = requests.Session()
	url = "https://api.twitch.tv/helix/streams?"

	for playa in twitch_streamers:
		url += "user_id=" + playa + "&"

	url = url[:-1]

	#print(url)

	try:
		r = s.get(url, headers=headers)
	except:
		sh.print_warning("### TWITCH REQUEST FAILED!!!")
		return
	
	#print("Poszło zapytanie - otrzymano " + str(r.status_code))
	response = json.loads(r.text)

	for playa in response["data"]:
		if not playa["user_id"] in twitch_streamers:
			#print("Nie znaleziono gracza w db")
			continue
		else:
			tmp = twitch_streamers[playa["user_id"]]
			
			if time.time()-tmp["last_seen"] < twitch_announcement_cooldown*60:
			#print(tmp["nickname"] + " - nie powiadamiam")
				tmp["last_seen"] = time.time()
				continue
			else:
				#print(tmp["nickname"] + " - alleluja!")
				tmp["last_seen"] = time.time()

				for ch in tmp["discord_channels"]:
					yield from client.send_message(discord.Object(id=ch), "{} właśnie streamuje na Twitchu! {}\n{}".format(tmp["nickname"], tmp["mention_group"], tmp["url"]))

t_twitch_announcements.channels = ["333"]
t_twitch_announcements.interval = twitch_check_frequency*60