from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleGetRecordAsMap(self, data):
    """ Get all dogtags the persona possesses """

    # TODO: Make Dogtags database
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetRecordAsMap")
    newPacket.set("PacketData", "TTL", "0")
    newPacket.set("PacketData", "state", "1")
    newPacket.set("PacketData", "values.{}", "0")

    Packet(newPacket).sendPacket(self, "rank", 0x80000000, self.CONNOBJ.plasmaPacketID, logger=logger)


def ReceivePacket(self, data, txn):
    if txn == 'GetRecordAsMap':
        HandleGetRecordAsMap(self, data)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown recp message (' + txn + ")", 2)
