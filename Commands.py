#-*- coding: utf-8 -*-
#!/usr/bin/env python

''' Kicks a list of users '''
def kick(bot, params):
	bot.say(bot.channels, "As you wish...")
	victims = params.split()
	print bot.channels

	for victim in victims:
		bot.kick(bot.channels, victim,
                         "This conversation can serve no purpose anymore."
                )

''' Leaves the channel '''
def suicide(bot, params):
	bot.say(bot.channels, "Sure. You'll never see me again...")
	bot.leave(bot.channels)

''' Hum... Clops at somthing '''
def clop(bot, params):
	names = params.split()
	if len(names)>0:
		bot.describe(bot.channels, "clops thinking about "
			+" and ".join(n for n in names)+".")
	else:
		bot.describe(bot.channels, "clops very hard. CLOP CLOP CLOP CLOP!")

''' Says moo '''
def say_moo(bot, params):
	bot.say(bot.channels, "Moooooo!")

''' Change karma '''
def karmic_change(bot, params):
        victim, change = params.split()
        bot.say(bot.channels, victim + " karma has been changed " + change)
