from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleSetPresenceStatus(self):
    # TODO: Make the Presence Status database
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "SetPresenceStatus")

    Packet(newPacket).sendPacket(self, "pres", 0x80000000, self.CONNOBJ.plasmaPacketID, logger=logger)


def ReceivePacket(self, data, txn):
    if txn == "SetPresenceStatus":
        HandleSetPresenceStatus(self)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown pres message (' + txn + ")", 2)
