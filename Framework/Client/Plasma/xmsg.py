from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleModifySettings(self, data):
    # TODO: Modify settings in database
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "ModifySettings")

    Packet(newPacket).sendPacket(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID, logger=logger)
    self.CONNOBJ.plasmaPacketID += 1

def HandleGetMessages(self, data):
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetMessages")
    newPacket.set("PacketData", "messages.[]", "0")

    Packet(newPacket).sendPacket(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID, logger=logger)
    self.CONNOBJ.plasmaPacketID += 1


def ReceivePacket(self, data, txn):
    if txn == 'ModifySettings':
        HandleModifySettings(self, data)
    elif txn == 'GetMessages':
        HandleGetMessages(self, data)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown xmsg message (' + txn + ")", 2)
