from Utilities.Packet import Packet


def HandleGetStats(self, data):
    # TODO: Make the Stats database
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetStats")

    requestedKeysNumber = int(data.get("PacketData", "keys.[]"))

    for i in range(requestedKeysNumber):
        requestedKey = data.get("PacketData", "keys." + str(i))

        toSend.set("PacketData", "stats." + str(i) + ".key", requestedKey)
        toSend.set("PacketData", "stats." + str(i) + ".value", "0.0")  # Until i won't do database for stats - it'll always return 0.0

    toSend.set("PacketData", "stats.[]", str(requestedKeysNumber))

    Packet(toSend).send(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetStats':
        HandleGetStats(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)
