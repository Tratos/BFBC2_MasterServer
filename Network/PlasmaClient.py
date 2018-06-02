from base64 import b64decode

from twisted.internet.protocol import Protocol

from DataClasses import Client
from Framework.Client.Plasma import *
from Globals import Clients
from Logger import Log
from Utilities.Packet import Packet


class HANDLER(Protocol):
    def __init__(self):
        self.CONNOBJ = None
        self.logger = Log("PlasmaClient", "\033[33;1m")
        self.logger_err = Log("PlasmaClient", "\033[33;1;41m")

        self.packetData = ""

    def connectionMade(self):
        self.ip, self.port = self.transport.client
        self.transport.setTcpNoDelay(True)

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] connected", 1)

        if self.CONNOBJ is None:
            self.CONNOBJ = Client()
            self.CONNOBJ.ipAddr = self.ip
            self.CONNOBJ.networkInt = self.transport
            Clients.append(self.CONNOBJ)

    def connectionLost(self, reason):
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] disconnected ", 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False
            Clients.remove(self.CONNOBJ)

        return

    def dataReceived(self, data):
        packet_type = data[:4]
        packet_checksum = data.split(data[12:])[0].split(packet_type)[1]
        packet_id = Packet(None).getPacketID(packet_checksum[:4])
        packet_length = packet_checksum[4:]
        packet_data = data.split(packet_type + packet_checksum)[1]

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "]<-- " + repr(data), 3)

        dataObj = Packet(packet_data).dataInterpreter()

        if packet_id == 0x80000000:  # Don't count it
            pass
        else:
            self.CONNOBJ.plasmaPacketID += 1

        try:
            dataEncrypted = dataObj.get("PacketData", "data")

            self.packetData += dataEncrypted.replace("%3d", "=")

            if len(self.packetData) == int(dataObj.get("PacketData", "size")):
                dataObj = Packet(b64decode(self.packetData) + "\x00").dataInterpreter()
                self.packetData = ""
                isValidPacket = True
            else:
                isValidPacket = False
        except:
            isValidPacket = True

        if Packet(data).verifyPacketLength(packet_length) and isValidPacket:
            TXN = dataObj.get("PacketData", "TXN")

            if packet_type == "fsys":
                fsys.ReceivePacket(self, dataObj, TXN)
            elif packet_type == "acct":
                acct.ReceivePacket(self, dataObj, TXN)
            elif packet_type == "asso":
                asso.ReceivePacket(self, dataObj, TXN)
            elif packet_type == "xmsg":
                xmsg.ReceivePacket(self, dataObj, TXN)
            elif packet_type == "pres":
                pres.ReceivePacket(self, dataObj, TXN)
            elif packet_type == "rank":
                rank.ReceivePacket(self, dataObj, TXN)
            elif packet_type == 'recp':
                recp.ReceivePacket(self, dataObj, TXN)
            else:
                self.logger_err.new_message(
                    "[" + self.ip + ":" + str(self.port) + ']<-- Got unknown message type (' + packet_type + ")", 2)
        elif not isValidPacket:
            pass
        else:
            self.logger_err.new_message("Warning: Packet Length is diffirent than the received data length!"
                                    "(" + self.ip + ":" + str(self.port) + "). Ignoring that packet...", 2)
