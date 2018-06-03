from Utilities.Packet import Packet


def HandleGetRecordAsMap(self):
    """ Get all dogtags the persona possesses """
    # TODO: Make Dogtags database

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetRecordAsMap")
    toSend.set("PacketData", "TTL", "0")
    toSend.set("PacketData", "state", "1")
    toSend.set("PacketData", "values.{}", "0")

    Packet(toSend).send(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleGetRecord(self):
    # TODO: find out what it is, and what to do with it

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetRecord")
    toSend.set("PacketData", "localizedMessage", "Record not found")
    toSend.set("PacketData", "errorContainer.[]", "0")
    toSend.set("PacketData", "errorCode", "5000")
    Packet(toSend).send(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetRecordAsMap':
        HandleGetRecordAsMap(self)
    elif txn == 'GetRecord':
        HandleGetRecord(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown recp message (' + txn + ")", 2)
