from ConfigParser import ConfigParser

from Utilities.Packet import Packet


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

    Packet(newPacket).sendPacket(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetStats':
        HandleGetStats(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)
