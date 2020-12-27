import asyncio
import datetime
import time

import os
import glob

import billy_shared as sh

start_time = time.time()
check = {}

@asyncio.coroutine
def check_flood(client, message):
	sh.debug("Checking for flood...")
	msg_limit = 5	# messages per channel
	time_limit = 5	# minutes
	
	if message.channel not in check:
		# channel not tracked yet
		check[message.channel] = {}
	
	if message.author not in check[message.channel]:
		# author on channel not tracked yet:
		check[message.channel][message.author] = {}
		check[message.channel][message.author]["timestamps"] = []
		check[message.channel][message.author]["warning_issued"] = False
	
	if len(check[message.channel][message.author]["timestamps"]) < msg_limit:
		# less than limit messages sent
		sh.debug("Message number " + str(len(check[message.channel][message.author]["timestamps"])+1))
		check[message.channel][message.author]["timestamps"].append(time.time())
		return False
	
	else:
		time_diff = time.time() - check[message.channel][message.author]["timestamps"][0]
		if time_diff > (time_limit*60):
			# message older than time limit
			sh.debug("Message number " + str(msg_limit) + "; deleted timestamp " + str(check[message.channel][message.author]["timestamps"][0]), message)
			check[message.channel][message.author]["timestamps"].pop(0)
			check[message.channel][message.author]["timestamps"].append(time.time())
			check[message.channel][message.author]["warning_issued"] = False
			return False
		else:
			if check[message.channel][message.author]["warning_issued"] == False:
				# scold user for spamming
				sh.debug("This user is spamming!")
				yield from client.send_message(message.channel, sh.mention(message) + "zamknij pizdę przez " + datetime.datetime.utcfromtimestamp((time_limit*60)-time_diff).strftime("%Mmin %Ss") + ". Spamuj w <#386148571529084929>")
				check[message.channel][message.author]["warning_issued"] = True
				return True
			else:
				# ...but just once
				sh.debug("This user is still spamming!")
				return False

@asyncio.coroutine
def check_flood_channel(client, message):
	sh.debug("Checking for channel flood...")
	msg_limit = 5    # messages per channel
	time_limit = 1    # minutes
	
	if message.channel not in check:
		# channel not tracked yet
		check[message.channel] = {}
		check[message.channel]["timestamps"] = []
		check[message.channel]["warning_issued"] = False
	
	if len(check[message.channel]["timestamps"]) < msg_limit:
		# less than limit messages sent
		sh.debug("Channel message number " + str(len(check[message.channel]["timestamps"])+1))
		check[message.channel]["timestamps"].append(time.time())
		return False
	
	else:
		time_diff = time.time() - check[message.channel]["timestamps"][0]
		if time_diff > (time_limit*60):
			# message older than time limit
			sh.debug("Channel message number " + str(msg_limit) + "; deleted timestamp " + str(check[message.channel]["timestamps"][0]), message)
			check[message.channel]["timestamps"].pop(0)
			check[message.channel]["timestamps"].append(time.time())
			check[message.channel]["warning_issued"] = False
			return False
		else:
			if check[message.channel]["warning_issued"] == False:
				# scold these idiots for spamming
				sh.debug("This channel is being flooded!")
				client.send_message(message.channel, "Weźcie wszyscy sklejcie pizdy przez " + datetime.datetime.utcfromtimestamp((time_limit*60)-time_diff).strftime("%Mmin %Ss") + ". Od spamowania jest <#386148571529084929>")
				check[message.channel]["warning_issued"] = True
				return True
			else:
				# ...but just once
				sh.debug("This channel is still being flooded!")
				return False

def check_channel_whitelist(client, message):
	deny_all = []
	# pecetgej, politbiuro, luzna_jazda, japabocie, japa_bocie
	allow_fulltext = ["318733700160290826", "174449535811190785", "316323075622961152", "319056762814595076", "386148571529084929"]
	# japabocie, japa_bocie, sesje_rpg, sun_world, kanau_fela
	unlimited = ["316323075622961152", "319056762814595076", "386148571529084929", "174541542923436032", "539154754631106584", "232881423604776960"]
	
	# default: disallow fulltext, enable flood control, enable bot
	permissions = {"fulltext" : False, "flood" : True, "disallow" : False}
	
	if str(message.channel).startswith("Direct Message"):
		sh.debug("Received message (private message):")
		permissions["flood"] = False
		permissions["fulltext"] = True
		
	else:
		if message.channel.id in deny_all:
			sh.debug("Received message (blacklisted channel):")
			permissions["disallow"] = True
			
		if message.channel.id in allow_fulltext:
			sh.debug("Received message (whitelisted channel):")
			permissions["fulltext"] = True
			
		if message.channel.id in unlimited:
			sh.debug("Received message (flood control inactive):")
			permissions["flood"] = False
		
	sh.debug("", message)
	
	return permissions


def check_uptime():
	list_of_files = glob.glob(sh.file_path("billy*.py"))
	latest_file = max(list_of_files, key=os.path.getmtime)
	
	ret = "Żyję już od " + str((datetime.datetime.today()-datetime.datetime.utcfromtimestamp(start_time)).days).zfill(2) + datetime.datetime.utcfromtimestamp(time.time()-start_time).strftime("d %Hh %Mmin %Ss") + "!\n"
	ret += "Ostatnia aktualizacja: " + datetime.datetime.fromtimestamp(int(os.path.getmtime(latest_file))).strftime('%Y-%m-%d %H:%M:%S') + " (" + latest_file + ")"
	return ret