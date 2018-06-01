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


def ReceivePacket(self, data, txn):
    if txn == 'GetRecordAsMap':
        HandleGetRecordAsMap(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown recp message (' + txn + ")", 2)
