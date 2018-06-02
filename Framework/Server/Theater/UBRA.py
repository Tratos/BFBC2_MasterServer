from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def ReceivePacket(self):
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))

    Packet(newPacket).sendPacket(self, "UBRA", 0x00000000, 0)
