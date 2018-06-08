#! python2.7

import sys

from Config import readFromConfig
from Database import Database
from Network import *
from Logger import Log

Log(None, None).clean_log()

try:
    from twisted.internet import ssl, reactor
    from twisted.internet.protocol import Factory, Protocol
    from twisted.web.server import Site
    from OpenSSL import SSL
except ImportError as importErr:
    Log("Init", "\033[37;41m").new_message("Fatal Error!\n"
                                           "Cannot import Twisted modules!\n"
                                           "Please install all required dependencies using\n"
                                           "`pip install -r requirements.txt`\n\n"
                                           "Additional error info:\n" + str(importErr), 0)
    sys.exit(1)

try:
    db = Database(True)
except Exception as DatabaseError:
    Log("Database", "\033[37;1;41m").new_message("Fatal Error! Cannot initialize database!\n\n"
                                                 "Additional error info:\n" + str(DatabaseError), 0)
    sys.exit(2)


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
        sys.exit(3)

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
        sys.exit(4)
    except Exception as BindError:
        Log("Init", "\033[33;1;41m").new_message("Fatal Error! Cannot bind socket to port: " +
                                                 readFromConfig("connection", "plasma_client_port") +
                                                 "\nMake sure that this port aren't used by another program!\n\n"
                                                 "Additional error info:\n" + str(BindError), 0)
        sys.exit(5)

    try:
        factory = Factory()
        factory.protocol = PlasmaServer.HANDLER
        reactor.listenSSL(int(readFromConfig("connection", "plasma_server_port")), factory, SSLContext)
        Log("PlasmaServer", "\033[36;1m").new_message("Created TCP Socket (now listening on port " +
                                                      str(readFromConfig("connection", "plasma_server_port")) + ")", 1)
    except KeyError:
        Log("Init", "\033[33;1;41m").new_message("Fatal Error! Cannot get Plasma Client port from config file!\n"
                                                 "You can fix that error by redownloading `config.ini`\n"
                                                 "Also make sure that `clientPort` contains only numbers.", 0)
        sys.exit(4)
    except Exception as BindError:
        Log("Init", "\033[33;1;41m").new_message("Fatal Error! Cannot bind socket to port: " +
                                                 readFromConfig("connection", "plasma_server_port") +
                                                 "\nMake sure that this port aren't used by another program!\n\n"
                                                 "Additional error info:\n" + str(BindError), 0)
        sys.exit(5)

    try:
        factoryTCP = Factory()
        factoryTCP.protocol = TheaterClient.TCPHandler
        reactor.listenTCP(int(readFromConfig("connection", "theater_client_port")), factoryTCP)
        Log("TheaterClient", "\033[35;1m").new_message("Created TCP Socket (now listening on port " +
                                                      str(readFromConfig("connection", "theater_client_port")) + ")", 1)
        reactor.listenUDP(int(readFromConfig("connection", "theater_client_port")), TheaterClient.UDPHandler())
        Log("TheaterClient", "\033[35;1m").new_message("Created UDP Socket (now listening on port " +
                                                      str(readFromConfig("connection", "theater_client_port")) + ")", 1)
    except KeyError:
        Log("Init", "\033[35;1;41m").new_message("Fatal Error! Cannot get Plasma Client port from config file!\n"
                                                 "You can fix that error by redownloading `config.ini`\n"
                                                 "Also make sure that `clientPort` contains only numbers.", 0)
        sys.exit(4)
    except Exception as BindError:
        Log("Init", "\033[35;1;41m").new_message("Fatal Error! Cannot bind socket to port: " +
                                                 readFromConfig("connection", "theater_client_port") +
                                                 "\nMake sure that this port aren't used by another program!\n\n"
                                                 "Additional error info:\n" + str(BindError), 0)
        sys.exit(5)

    try:
        factoryTCP = Factory()
        factoryTCP.protocol = TheaterServer.TCPHandler
        reactor.listenTCP(int(readFromConfig("connection", "theater_server_port")), factoryTCP)
        Log("TheaterServer", "\033[32;1m").new_message("Created TCP Socket (now listening on port " +
                                                      str(readFromConfig("connection", "theater_server_port")) + ")", 1)
        reactor.listenUDP(int(readFromConfig("connection", "theater_server_port")), TheaterServer.UDPHandler())
        Log("TheaterServer", "\033[32;1m").new_message("Created UDP Socket (now listening on port " +
                                                      str(readFromConfig("connection", "theater_server_port")) + ")", 1)
    except KeyError:
        Log("Init", "\033[35;1;41m").new_message("Fatal Error! Cannot get Plasma Client port from config file!\n"
                                                 "You can fix that error by redownloading `config.ini`\n"
                                                 "Also make sure that `clientPort` contains only numbers.", 0)
        sys.exit(4)
    except Exception as BindError:
        Log("Init", "\033[35;1;41m").new_message("Fatal Error! Cannot bind socket to port: " +
                                                 readFromConfig("connection", "theater_server_port") +
                                                 "\nMake sure that this port aren't used by another program!\n\n"
                                                 "Additional error info:\n" + str(BindError), 0)
        sys.exit(5)

    try:
        site = Site(WebServer.Handler())
        reactor.listenTCP(int(readFromConfig("connection", "http_server_port")), site)
        Log("WebServer", "\033[36m").new_message("Created TCP Socket (now listening on port " + str(readFromConfig("connection", "http_server_port")) + ")", 1)
    except KeyError:
        Log("Init", "\033[35;1;41m").new_message("Fatal Error! Cannot get Plasma Client port from config file!\n"
                                                 "You can fix that error by redownloading `config.ini`\n"
                                                 "Also make sure that `http_server_port` contains only numbers.", 0)
        sys.exit(4)
    except Exception as BindError:
        Log("Init", "\033[35;1;41m").new_message("Fatal Error! Cannot bind socket to port: " +
                                                 readFromConfig("connection", "http_server_port") +
                                                 "\nMake sure that this port aren't used by another program!\n\n"
                                                 "Additional error info:\n" + str(BindError), 0)
        sys.exit(5)

    Log("Init", "\033[37m").new_message("Finished initialization! Ready for receiving incoming connections...", 0)

    reactor.run()


if __name__ == '__main__':
    Start()
