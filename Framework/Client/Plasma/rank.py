from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleGetStats(self, data):
    # TODO: Make the Stats database

    requestedKeysNumber = int(data.get("PacketData", "keys.[]"))

    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetStats")

    for i in range(requestedKeysNumber):
        requestedKey = data.get("PacketData", "keys." + str(i))

        newPacket.set("PacketData", "stats." + str(i) + ".key", requestedKey)
        newPacket.set("PacketData", "stats." + str(i) + ".value",
                      "0.0")  # Until i won't do database for stats - it'll always return 0.0

    newPacket.set("PacketData", "stats.[]", str(requestedKeysNumber))

    Packet(newPacket).sendPacket(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID, logger=logger)


def ReceivePacket(self, data, txn):
    if txn == 'GetStats':
        HandleGetStats(self, data)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)
