# Billy Mays

This is just a Discord bot written for my personal use. It's very sloppily written - please don't judge. Also lots of hardcoded Polish strings and whatnot. This repo serves mainly as my backup, but maybe you'll find it of some use as well.

**WARNING**: This bot was written to be used on first-gen Raspberry Pi, thus it relies on outdated technology. **Python 3.6** (or older) **and discord.py 0.16.12 are REQUIRED**.

My main goal was to sort of port IRC bot Sopel to Discord. Sopel modules can be used here to some extent (a few of these are included in repo), but this will require modifications.

`kathai.py` is an offshoot of Billy that randomly says some weird thing in chat, gives reactions, etc. Not really relevant. If you want to use it, please set `kathai_key` value in the **config.py** file. I haven't used this thing in some time, it might not work anymore.

## Requirements

As written above - you need to use Python major version up to 3.6. If you have a newer Python version on your system, you might need to altinstall Python 3.6 alongside your main version, Here are some of the required `pip` packets (this list might not be exhaustive - sorry!)

```
bs4
discord=0.16.12
cleverwrap
colorama
emoji
requests
unidecode
wolframalpha
ftfy
Pillow
```

Also required is the `MemePy` library, please download it manually and put it in the `_MemePy` folder (note the underscore). https://github.com/yojo2/MemePy

Note that vanilla discord.py `0.16.12` will not work anymore due to changes on the Discord server side. Please fix it manually: https://github.com/Rapptz/discord.py/commit/10d1feb3efd699500f1adb4cee8d965518b0d061

## App config

To make full use of Billy's functions, please create a `config.py` file with following contents:

```
billy_key = ""
cleverbot_key = ""
wolfram_key = ""
twitch_key = ""
twitch_secret = ""
bot_owners = [""]
```

Please fill in the empty fields accordingly. You can do it! (the bot should be able to start with just `billy_key` filled in)

## Command line parameters

* `-b` or `--debug` - **show simple debug messages in console**
Self-explanatory. Not as useful as it might sound, but still.

* `-l` or `--list` - **lists all functions imported from modules**
On bot startup, it prints all of the functions that were activated from available Billy modules. This is a very long list which you probably don't ever need to see, which is why this is a separate option from `-b`.

* `-n` or `--nostats` - **disable statistics module**
Launches the bot as normal, but with statistics completely disabled. `billy_c_stats.py` is not loaded. Generating statistics tends to kill the script without warning (dunno why, maybe it's exceeding allowed execution time?), so if you want, you can launch them in a seperate bot instance.

* `-s` or `--stats` - **launch statistics module ONLY**
Only the `billy_c_stats.py` module is loaded, and nothing else. As stated above - you can run one bot instance with parameter `-n` and the other with `-s`, so that in case the stats generation fails, the main part of the bot keeps running.

* `-d` or `--dev` - **enables developer mode**
Enables options `--debug` and `--list`. None of the standard Billy modules (`billy_c_*.py`) are loaded. Instead, it loads all modules with filename `billy_c_dev_*.py`. The basic idea is that you rename the module you're working on accordingly, and then launch the bot in developer mode. Please note that every function gets a `dev_` prefix (for example, `.dev_uptime` instead of `.uptime`). Only the bot owners (specified in `config.py`) can use the bot in this mode.

## Automatic restart

For some reason, this bot can shut down itself without any warning or error. I can't figure it out for the life of me, I blame it on the Raspberry Pi. I've worked around it creating a shell script:

```
while true
do
	python3 /path/to/file.py
	now="$(date)"
	echo -e "\e[91m$now Script ended! Restarting in 10 secs...\e[39m"
	sleep 10
done
```

(please remember that Windows uses \r\n instead of \n...)

## Others

This project is still mantained and developed, but I'm kinda lazy. No major updates planned.
