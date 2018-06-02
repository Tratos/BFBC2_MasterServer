import re

from twisted.internet.protocol import Protocol, DatagramProtocol

from Framework.Client.Theater import *
from Logger import Log
from Utilities.Packet import Packet


class TCPHandler(Protocol):
    def __init__(self):
        self.CONNOBJ = None
        self.logger = Log("TheaterClient", "\033[35;1m")
        self.logger_err = Log("TheaterClient", "\033[35;1;41m")

    def connectionMade(self):
        self.ip, self.port = self.transport.client
        self.transport.setTcpNoDelay(True)

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] connected", 1)

    def connectionLost(self, reason):
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] disconnected ", 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False

        return

    def dataReceived(self, data):
        packet_type = data[:4]
        packet_data = data[12:]

        dataObj = Packet(packet_data).dataInterpreter()
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "]<-- " + repr(data), 3)

        if self.CONNOBJ is not None:
            self.CONNOBJ.theaterPacketID += 1

        if packet_type == 'CONN':
            CONN.ReceiveRequest(self, dataObj)
        elif packet_type == 'USER':
            USER.ReceiveRequest(self, dataObj)
        elif packet_type == 'LLST':
            LLST.ReceiveRequest(self, dataObj)
        elif packet_type == 'GLST':
            GLST.ReceiveRequest(self, dataObj)
        else:
            self.logger_err.new_message(
                "[" + self.ip + ":" + str(self.port) + ']<-- Got unknown message type (' + packet_type + ")", 2)


class UDPHandler(DatagramProtocol):
    def __init__(self):
        self.logger = Log("TheaterClient", "\033[35;1m")
        self.logger_err = Log("TheaterClient", "\033[35;1;41m")

    def datagramReceived(self, datagram, addr):
        packet_type = datagram[:4]
        packet_data = datagram[12:]

        dataObj = Packet(packet_data).dataInterpreter()
        self.logger.new_message("[" + addr[0] + ":" + str(addr[1]) + "]<-- " + repr(datagram), 3)

        if packet_type == 'ECHO':
            ECHO.ReceiveRequest(self, dataObj, addr)
        else:
            self.logger_err.new_message("[" + addr[0] + ":" + str(addr[1]) + "][UDP] Received unknown packet type! (" + packet_type + ")", 2)
