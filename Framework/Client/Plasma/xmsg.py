from Utilities.Packet import Packet


def HandleModifySettings(self):
    # TODO: Modify settings in database

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "ModifySettings")

    Packet(toSend).send(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleGetMessages(self):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetMessages")
    toSend.set("PacketData", "messages.[]", "0")

    Packet(toSend).send(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'ModifySettings':
        HandleModifySettings(self)
    elif txn == 'GetMessages':
        HandleGetMessages(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown xmsg message (' + txn + ")", 2)
