from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def HandleModifySettings(self):
    # TODO: Modify settings in database
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "ModifySettings")

    Packet(newPacket).sendPacket(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleGetMessages(self):
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetMessages")
    newPacket.set("PacketData", "messages.[]", "0")

    Packet(newPacket).sendPacket(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'ModifySettings':
        HandleModifySettings(self)
    elif txn == 'GetMessages':
        HandleGetMessages(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown xmsg message (' + txn + ")", 2)
