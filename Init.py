#! python2.7

import sys

from Config import readFromConfig
from Network import *
from Logger import Log

try:
    from twisted.internet import ssl, reactor
    from twisted.internet.protocol import Factory, Protocol
    from OpenSSL import SSL
except ImportError as importErr:
    Log("Init", "\033[37;41m").new_message("Fatal Error!\n"
                                           "Cannot import Twisted modules!\n"
                                           "Please install all required dependencies using\n"
                                           "`pip install -r requirements.txt`\n\n"
                                           "Additional error info:\n" + str(importErr), 0)
    sys.exit(1)


def Start():
    Log("Init", "\033[37m").new_message("Initializing Battlefield: Bad Company 2 Master Server Emulator...", 0)

    try:
        SSLContext = ssl.DefaultOpenSSLContextFactory(readFromConfig("SSL", "priv_key_path"),
                                                      readFromConfig("SSL", "cert_file_path"))
        Log("Init", "\033[37m").new_message("Successfully created SSL Context!", 2)
    except Exception as SSLErr:
        Log("Init", "\033[37;41m").new_message("Fatal Error!\n"
                                               "Failed to create SSL Context!\n"
                                               "Make sure that you installed all required modules using\n"
                                               "`pip install -r requirements.txt\n\n"
                                               "Additional error info:\n" + str(SSLErr), 0)
        sys.exit(2)

    try:
        factory = Factory()
        factory.protocol = PlasmaClient.HANDLER
        reactor.listenSSL(int(readFromConfig("connection", "plasma_client_port")), factory, SSLContext)
        Log("PlasmaClient", "\033[33;1m").new_message("Created TCP Socket (now listening on port " +
                                                      str(readFromConfig("connection", "plasma_client_port")) + ")", 1)
    except KeyError:
        Log("Init", "\033[33;1;41m").new_message("Fatal Error! Cannot get Plasma Client port from config file!\n"
                                                 "You can fix that error by redownloading `config.ini`\n"
                                                 "Also make sure that `clientPort` contains only numbers.", 0)
        sys.exit(3)
    except Exception as BindError:
        Log("Init", "\033[33;1;41m").new_message("Fatal Error! Cannot bind socket to port: " +
                                                 readFromConfig("connection", "plasma_client_port") +
                                                 "\nMake sure that this port aren't used by another program!\n\n"
                                                 "Additional error info:\n" + str(BindError), 0)
        sys.exit(4)

    Log("Init", "\033[37m").new_message("Finished initialization! Ready for receiving incoming connections...", 0)

    reactor.run()


if __name__ == '__main__':
    Start()
