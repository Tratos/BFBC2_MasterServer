from twisted.internet.protocol import Protocol

from DataClasses import Client
from Framework.Client.Plasma import *
from Globals import Clients
from Logger import Log
from Utilities.Packet import Packet

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


class HANDLER(Protocol):
    def __init__(self):
        self.CONNOBJ = None

    def connectionMade(self):
        self.ip, self.port = self.transport.client
        self.transport.setTcpNoDelay(True)

        logger.new_message("[" + self.ip + ":" + str(self.port) + "] connected", 1)

        if self.CONNOBJ is None:
            self.CONNOBJ = Client()
            self.CONNOBJ.ipAddr = self.ip
            self.CONNOBJ.networkInt = self.transport
            self.CONNOBJ.plasmaPacketID = 1
            Clients.append(self.CONNOBJ)

    def connectionLost(self, reason):
        logger.new_message("[" + self.ip + ":" + str(self.port) + "] disconnected ", 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False
            Clients.remove(self.CONNOBJ)

        return

    def dataReceived(self, data):
        packet_type = data[:4]
        packet_checksum = data.split(packet_type)[1].split("TXN")[0]
        packet_id = packet_checksum[:4]
        packet_length = packet_checksum[4:]
        packet_data = data.split(packet_type + packet_checksum)[1]

        logger.new_message("[" + self.ip + ":" + str(self.port) + "]<-- " + repr(data), 3)

        dataObj = Packet(packet_data).dataInterpreter()

        if Packet(data).verifyPacketLength(packet_length):
            TXN = dataObj.get("PacketData", "TXN")

            if packet_type == "fsys":
                fsys.ReceivePacket(self, dataObj, TXN)
            elif packet_type == "acct":
                acct.ReceivePacket(self, dataObj, TXN)
            else:
                logger_err.new_message(
                    "[" + self.ip + ":" + str(self.port) + ']<-- Got unknown message type (' + packet_type + ")", 2)
        else:
            logger_err.new_message("Warning: Packet Length is diffirent than the received data length!"
                                   "(" + self.ip + ":" + self.port + "). Ignoring that packet...", 2)
