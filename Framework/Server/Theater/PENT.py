from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def ReceivePacket(self, data):
    # TODO: Remove player from Joining Players and add player to Active Players

    newPacketData = ConfigParser()
    newPacketData.optionxform = str
    newPacketData.add_section("PacketData")
    newPacketData.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    newPacketData.set("PacketData", "PID", str(data.get("PacketData", "PID")))

    Packet(newPacketData).sendPacket(self, "PENT", 0x00000000, 0)
