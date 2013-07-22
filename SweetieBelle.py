#!/usr/bin/env python

import sys
import ConfigParser

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log


''' Our friendly bot main class '''
class SweetieBelle(irc.IRCClient):

	nickname = "SweetieBelle"
	realname = "Sweetie Belle"

	# TODO : authentification
	# username = ""
	# password = ""

	log_file = "sweetie_log"

	''' Called after sucessfully signing on to the server '''
	def signedOn(self):
		self.join(self.factory.channels)
		self.say(self.channels, "Bonjour !")

	''' Callback triggered each time a mesage is recieved '''
	def privmsg(self, user, channel, message):
		if channel in self.channels and self.nickname in message:
			self.say(channel, "On me parle ?")


''' Connexion factory, handles default channels '''
class IRCFactory(protocol.ReconnectingClientFactory):

	protocol = SweetieBelle

	def __init__(self, channels):
		self.channels = channels 


''' Creates a new bot instance that connects to the server '''
def startSweetie():

	config = ConfigParser.RawConfigParser()
	config.read('bot.cfg')
	SweetieBelle.server_host = config.get("connection", "server")
	SweetieBelle.server_port = config.getint("connection", "port")
	SweetieBelle.channels = config.get("connection", "channels")

	print "Connecting to " + SweetieBelle.server_host + ":" + str(SweetieBelle.server_port) 
	reactor.connectTCP(
		SweetieBelle.server_host,
		SweetieBelle.server_port,
		IRCFactory(SweetieBelle.channels)
		)
	log.startLogging(sys.stdout)
	print "Connexion established!"
	reactor.run()

if __name__ == '__main__':
	startSweetie()