# coding: utf-8

from bot import settings

import sys
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log


class SweetieBelle(irc.IRCClient):
    """ Our friendly bot class.
    """

    def connectionMade(self):
        """ Sets bot identity connection to the IRC server is established.
        """
        self.nickname = self.factory.nickname
        self.username = self.factory.nickname
        self.realname = self.factory.realname
        irc.IRCClient.connectionMade(self)

    def signedOn(self):
        """ Callback once the bot has successfully logged in the server.
        """
        for _, channel in self.factory.channels.items():
            print 'Joining {}'.format(channel['name'], channel.get('password'))
            self.join(channel.get('name'), channel.get('password'))

    def joined(self, channel):
        """ Sending a greeting message when joining a chan.
        """
        self.say(channel, "Hello to you {}!".format(channel))


class SweetieFactory(protocol.ReconnectingClientFactory):
    """ Client factory class.
    As a new client is initiated each time the bot has to reconnect, client
    properties are stored in this factory to begin with.
    """
    protocol = SweetieBelle

    def __init__(self, **kwargs):
        self.nickname = kwargs.get('nickname') or settings.BOT_NAME
        self.username = kwargs.get('username') or settings.BOT_NAME
        self.realname = kwargs.get('realname') or settings.BOT_REALNAME

        self.channels = kwargs.get('channels') or settings.CHANNELS


def startSweetie(**kwargs):
    log.startLogging(sys.stdout)
    reactor.connectTCP(kwargs.get('address') or settings.IRC_SERVER,
                       kwargs.get('port') or settings.SERVER_PORT,
                       SweetieFactory(**kwargs))
    reactor.run()
