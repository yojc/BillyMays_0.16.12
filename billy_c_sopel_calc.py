# coding=utf-8
"""
calc.py - Sopel Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from billy_sopel_calculation import eval_equation
import billy_sopel_web as web
import sys
import asyncio
import billy_shared as sh

if sys.version_info.major >= 3:
	unichr = chr


BASE_TUMBOLIA_URI = 'https://tumbolia-two.appspot.com/'

@asyncio.coroutine
def c_calc(client, message):
	"""Evaluate some calculation."""
	if len(sh.get_args(message)) == 0:
		yield from client.send_message(message.channel, "Nothing to calculate.")
		return
	# Account for the silly non-Anglophones and their silly radix point.
	eqn = sh.get_args(message).replace(',', '.')
	try:
		result = eval_equation(eqn)
		result = "{:.10g}".format(result)
	except ZeroDivisionError:
		result = "Division by zero is not supported in this universe."
	except Exception as e:
		result = "{error}: {msg}".format(error=type(e), msg=e)
	yield from client.send_message(message.channel, sh.mention(message) + result)

c_calc.command = r"(c|calc)"
c_calc.desc = "Kalkulator"


@asyncio.coroutine
def c_py(client, message):
	"""Evaluate a Python expression."""
	if len(sh.get_args(message)) == 0:
		yield from client.send_message(message.channel, sh.mention(message) + "Need an expression to evaluate")
		return

	query = sh.get_args(message)
	uri = BASE_TUMBOLIA_URI + 'py/'
	answer = web.get(uri + web.quote(query))
	if answer:
		#bot.say can potentially lead to 3rd party commands triggering.
		yield from client.send_message(message.channel, sh.mention(message) + answer)
	else:
		yield from client.send_message(message.channel, sh.mention(message) + 'Sorry, no result.')

c_py.command = r"py"
c_py.desc = "Wykonaj kod Pythonowy"