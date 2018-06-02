from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def ReceivePacket(self, data):
    allowed = data.get("PacketData", "ALLOWED")

    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")

    if str(allowed) == "1":
        # TODO: Add player to JOINING_PLAYERS
        pass

    newPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    Packet(newPacket).sendPacket(self, "EGRS", 0x00000000, 0)
