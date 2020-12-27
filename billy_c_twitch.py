import discord
import random
import asyncio

import requests
import json
import time

import billy_shared as sh
from config import twitch_key, twitch_secret


politbiuro_main_channel = "174449535811190785"
politbiuro_ograch = "639853618568232982"
politbiuro_retro = "305100969191014404"
politbiuro_japabocie = "386148571529084929"

twitch_check_frequency = 1 # minutes
twitch_bot_start_timeout = 5 # minutes
twitch_announcement_cooldown = 19.5 # minutes
twitch_start_time = time.time() - twitch_bot_start_timeout*60
oauth_token = ""

# to find out the oauth-token
# curl -X POST "https://id.twitch.tv/oauth2/token?client_id=[twitch-id]&client_secret=[client-secret]&grant_type=client_credentials"

# to find out the user ID
# curl -H "client-id: n39cbw7gz4kzblf6k4u1p2lxx87jib" -H "authorization: Bearer k8z2zdqm4v2952hs5o04t717tzp4mx" https://api.twitch.tv/helix/users?login=nevka_

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
	},

	"449776925" : { 
		"nickname" : "nevka", 
		"url" : "https://www.twitch.tv/nevka_", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&718134655945015346>"
	}

	#"40426372" : { 
	#	"nickname" : "Teb", 
	#	"url" : "https://www.twitch.tv/Tebeg", 
	#	"last_seen" : time.time(),
	#	"discord_channels" : [politbiuro_japabocie]
	#}
}

def refresh_oauth_token():
	global twitch_key
	global twitch_secret
	global oauth_token

	s = requests.Session()
	url="https://id.twitch.tv/oauth2/token?client_id=" + twitch_key + "&client_secret=" + twitch_secret + "&grant_type=client_credentials"
	
	try:
		r = s.post(url, timeout=12.05)
	except:
		sh.print_warning("### TWITCH OAUTH REQUEST FAILED!!!", date=True)
		return

	response = json.loads(r.text)

	if "access_token" in response:
		oauth_token = "Bearer " + response["access_token"]
		sh.print_warning("### TWITCH New OAuth token", date=True)
	else:
		sh.print_warning("### TWITCH Malformed OAuth token?", date=True)

	sh.print_warning(json.dumps(response))


@asyncio.coroutine
def t_twitch_announcements(client, channels):
	global twitch_key
	global twitch_streamers
	global oauth_token

	#sh.print_warning("### TWITCH TEST ### ", date=True)

	if not oauth_token:
		refresh_oauth_token()

	#print(oauth_token)
	headers = {"client-id": twitch_key, "authorization": oauth_token}
	s = requests.Session()
	url = "https://api.twitch.tv/helix/streams?"

	for playa in twitch_streamers:
		url += "user_id=" + playa + "&"

	url = url[:-1]

	#print(url)

	try:
		r = s.get(url, headers=headers, timeout=12.05)
	except:
		sh.print_warning("### TWITCH REQUEST FAILED!!!", date=True)
		return
	
	#print("Poszło zapytanie - otrzymano " + str(r.status_code))
	response = json.loads(r.text)

	if "status" in response and response["status"] is not 200:
		if response["status"] == 401:
			sh.print_warning("### TWITCH Auth error (OAuth token expired?)", date=True)
			refresh_oauth_token()
			sh.print_warning(json.dumps(response))
		else:
			sh.print_warning("### TWITCH Unexpected error", date=True)
			sh.print_warning(json.dumps(response))
	elif "data" in response:
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
	else:
		sh.print_warning("### TWITCH Malformed data received?", date=True)
		sh.print_warning(json.dumps(response))

t_twitch_announcements.channels = ["333"]
t_twitch_announcements.interval = twitch_check_frequency*60