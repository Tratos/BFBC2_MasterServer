from Utilities.Packet import Packet


def HandleSetPresenceStatus(self):
    # TODO: Make the Presence Status database

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "SetPresenceStatus")

    Packet(toSend).send(self, "pres", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == "SetPresenceStatus":
        HandleSetPresenceStatus(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown pres message (' + txn + ")", 2)
