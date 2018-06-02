from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def HandleGetRecordAsMap(self):
    """ Get all dogtags the persona possesses """

    # TODO: Make Dogtags database
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetRecordAsMap")
    newPacket.set("PacketData", "TTL", "0")
    newPacket.set("PacketData", "state", "1")
    newPacket.set("PacketData", "values.{}", "0")

    Packet(newPacket).sendPacket(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)

def HandleGetRecord(self):
    # TODO: find out what it is, and what to do with it

    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetRecord")
    newPacket.set("PacketData", "localizedMessage", "Record not found")
    newPacket.set("PacketData", "errorContainer.[]", "0")
    newPacket.set("PacketData", "errorCode", "5000")
    Packet(newPacket).sendPacket(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetRecordAsMap':
        HandleGetRecordAsMap(self)
    elif txn == 'GetRecord':
        HandleGetRecord(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown recp message (' + txn + ")", 2)
