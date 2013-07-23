#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, re
import ConfigParser
import Commands

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log


''' Our friendly bot main class '''
class SweetieBelle(irc.IRCClient):

	''' Called after sucessfully signing on to the server '''
	def signedOn(self):
		self.join(self.factory.channels)
		self.say(self.channels, "Bonjour !")

	''' Callback triggered each time a mesage is recieved '''
	def privmsg(self, user, channel, message):
		author, _, host = user.partition('!')

		if message.startswith(self.nickname) or channel==self.nickname:
			# Stripping the message of the bot nickname
			message = re.sub(r'^%s[.,>:;!?]*\s*' % 
                                         re.escape(self.nickname),
                                         '',
                                         message
                        )
			command, _, params = message.partition(" ")
			
			if command in SweetieBelle.commands:
				SweetieBelle.commands[command](self, params)
			else:
				self.say(channel,
					"I'm sorry " + author +
                                         " but I don't understand your request."
                                )


''' Connection factory, handles default channels '''
class IRCFactory(protocol.ReconnectingClientFactory):

	protocol = SweetieBelle

	def __init__(self, channels):
		self.channels = channels 

'''Loads config from a file using ConfigParser ''' 
def load_config(filename):
	config = ConfigParser.RawConfigParser()
	config.read(filename)
	SweetieBelle.server_host = config.get("connection", "server")
	SweetieBelle.server_port = config.getint("connection", "port")
	SweetieBelle.channels = config.get("connection", "channels")
	SweetieBelle.nickname = config.get("identity", "nickname")
	SweetieBelle.realname = config.get("identity", "realname")
	# TODO : authentification
	SweetieBelle.logfile = config.get("local", "logfile")


''' Creates a new bot instance that connects to the server '''
def startSweetie():

	log.startLogging(sys.stdout)

	print "Loading configuration file"
	load_config('bot.cfg')

	print "Connecting to " + SweetieBelle.server_host + ":\
        " + str(SweetieBelle.server_port) 
	print "Joining channels " + SweetieBelle.channels
	reactor.connectTCP(
		SweetieBelle.server_host,
		SweetieBelle.server_port,
		IRCFactory(SweetieBelle.channels)
		)
	print "Connexion established!"

	SweetieBelle.commands = {
		'kick': Commands.kick,
		'moo': Commands.say_moo,
                'karma': Commands.karmic_change,
	}

	reactor.run()

if __name__ == '__main__':
	startSweetie()
