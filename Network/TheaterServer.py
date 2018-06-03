import re

from twisted.internet.protocol import Protocol, DatagramProtocol

from Framework.Server.Theater import *
from Logger import Log
from Utilities.Packet import Packet


class TCPHandler(Protocol):
    def __init__(self):
        self.CONNOBJ = None
        self.logger = Log("TheaterServer", "\033[32;1m")
        self.logger_err = Log("TheaterServer", "\033[32;1;41m")


    def connectionMade(self):
        self.ip, self.port = self.transport.client
        self.transport.setTcpNoDelay(True)

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] connected", 1)

    def connectionLost(self, reason):
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] disconnected ", 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False
            del self

        return

    def dataReceived(self, data):
        packet_type = data[:4]

        if data.count("UBRA") == 2:
            multiUBRA = True
        else:
            multiUBRA = False

        packets = data.split('\n\x00')

        dataObjs = []

        if len(packets) > 2:
            for packet in packets:
                fixedPacketType = packet[:4]
                fixedPacket = packet[12:]

                if len(fixedPacket) == 0:
                    break

                if multiUBRA and fixedPacket.count("START=0") != 0:
                    pass
                else:
                    dataObjs.append({"data": Packet(fixedPacket + "\n\x00").dataInterpreter(), "type": fixedPacketType})
        else:
            dataObjs.append({"data": Packet(packets[0][12:] + "\n\x00").dataInterpreter(), "type": packet_type})

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "]<-- " + repr(data), 3)

        if self.CONNOBJ is not None:
            self.CONNOBJ.theaterPacketID += 1

        for dataObj in dataObjs:

            if dataObj['type'] == 'CONN':
                CONN.ReceiveRequest(self, dataObj['data'])
            elif dataObj['type'] == 'USER':
                USER.ReceiveRequest(self, dataObj['data'])
            elif dataObj['type'] == 'CGAM':
                CGAM.ReceiveRequest(self, dataObj['data'])
            elif dataObj['type'] == 'UBRA':
                UBRA.ReceivePacket(self, multiUBRA)
            elif dataObj['type'] == 'UGAM':
                UGAM.ReceivePacket(self, dataObj['data'])
            elif dataObj['type'] == 'UGDE':
                UGDE.ReceivePacket(self, dataObj['data'])
            elif dataObj['type'] == 'EGRS':
                EGRS.ReceivePacket(self, dataObj['data'])
            elif dataObj['type'] == 'PENT':
                PENT.ReceivePacket(self, dataObj['data'])
            else:
                self.logger_err.new_message(
                    "[" + self.ip + ":" + str(self.port) + ']<-- Got unknown message type (' + dataObj['type'] + ")", 2)


class UDPHandler(DatagramProtocol):
    def __init__(self):
        self.logger = Log("TheaterServer", "\033[32;1m")
        self.logger_err = Log("TheaterServer", "\033[32;1;41m")

    def datagramReceived(self, datagram, addr):
        packet_type = datagram[:4]
        packet_data = datagram[12:]

        dataObj = Packet(packet_data).dataInterpreter()
        self.logger.new_message("[" + addr[0] + ":" + str(addr[1]) + "]<-- " + repr(datagram), 3)

        if packet_type == 'ECHO':
            ECHO.ReceiveRequest(self, dataObj, addr)
        else:
            self.logger_err.new_message("[" + addr[0] + ":" + str(addr[1]) + "][UDP] Received unknown packet type! (" + packet_type + ")", 2)
