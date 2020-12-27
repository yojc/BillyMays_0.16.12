import random
import asyncio

import billy_shared as sh

# -------------------------------------
# do wykonania o określonych godzinach
# -------------------------------------


#@asyncio.coroutine
#def t_pope_time(client, channels):
#	choices = ["zapraszam wszystkich na kremówki", "wybiła godzina papieska", "Jan Paweł 2, w moim sercu zawsze 1", "Jan Paweł II był wielkim człowiekiem", "Jan Paweł 2 Gloria Matki Dziewicy"]
#	barka = [("Pan kiedyś stanął nad brzegiem,\n" +
#		"Szukał ludzi gotowych pójść za Nim;\n" +
#		"By łowić serca\n" +
#		"Słów Bożych prawdą.\n\n" +
#		"Ref.: \n" +
#		"O Panie, to Ty na mnie spojrzałeś,\n" +
#		"Twoje usta dziś wyrzekły me imię.\n" +
#		"Swoją barkę pozostawiam na brzegu,\n" +
#		"Razem z Tobą nowy zacznę dziś łów."), (("O"*random.randint(3, 10)) + " P" + ("A"*random.randint(5,15)) + "NI" + ("E"*random.randint(5,15)))]
#	
#	reply = random.choice([random.choice(choices), random.choice(barka)])
#	
#	for ch in channels:
#		#yield from client.send_message(ch, reply)
#		yield from client.send_message(ch, "Jebać PiS")
#
#t_pope_time.channels = ["174449535811190785"]
#t_pope_time.time = "21:37"

def random_a():
	return "A"*random.randint(3,7)

@asyncio.coroutine
def t_trzytrzytrzy(client, channels):
	
	choices = ["https://www.youtube.com/watch?v=WX8ZeZJqOE0", "https://www.youtube.com/watch?v=rRctiUI8pmE", "https://www.youtube.com/watch?v=IJKWUTgrE2g", "https://www.youtube.com/watch?v=UskQs90Y2TE", "pac"]
	
	reply = random.choice(choices)
	for ch in channels:
		if random.random() < 0.075:
			if reply == "pac":
				yield from client.send_message(ch, "O K{}T{}J\nTO TY MNIE POPAC{}Ł{}Ś".format(random_a(), random_a(), random_a(), random_a()))
			else:
				yield from client.send_message(ch, reply)

t_trzytrzytrzy.channels = ["174449535811190785"]
t_trzytrzytrzy.time = "3:33"
