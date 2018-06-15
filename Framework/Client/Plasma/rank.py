from Database import Database
from Utilities.Packet import Packet

db = Database()


def HandleGetStats(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetStats")

    requestedKeysNumber = int(data.get("PacketData", "keys.[]"))
    requestedKeys = []

    for i in range(requestedKeysNumber):
        requestedKeys.append(data.get("PacketData", "keys." + str(i)))

    keysValues = db.GetStatsForPersona(self.CONNOBJ.personaID, requestedKeys)

    for i in range(len(requestedKeys)):
        toSend.set("PacketData", "stats." + str(i) + ".key", keysValues[i]['name'])
        toSend.set("PacketData", "stats." + str(i) + ".value", keysValues[i]['value'])

    toSend.set("PacketData", "stats.[]", str(requestedKeysNumber))

    Packet(toSend).send(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetStats':
        HandleGetStats(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)
