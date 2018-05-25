from twisted.internet.protocol import Protocol

from Logger import Log

logger = Log("PlasmaClient", "\33[36m")


class HANDLER(Protocol):
    def __init__(self):
        self.CONNOBJ = None

    def connectionMade(self):
        self.ip, self.port = self.transport.client
        self.transport.setTcpNoDelay(True)

        logger.new_message("Got connection from " + self.ip + ":" + str(self.port), 1)

    def connectionLost(self, reason):
        logger.new_message("Lost connection to " + self.ip + ":" + str(self.port), 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False

        return

    def readConnectionLost(self):
        logger.new_message("Lost connection to " + self.ip + ":" + str(self.port), 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False

        self.transport.loseConnection()
        return

    def writeConnectionLost(self):
        logger.new_message("Closed connection to " + self.ip + ":" + str(self.port), 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False

        self.transport.loseConnection()

        return

    def dataReceived(self, data):
        print(repr(data))
