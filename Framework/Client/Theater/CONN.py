from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    newPacketData = ConfigParser()
    newPacketData.optionxform = str
    newPacketData.add_section("PacketData")

    tid = data.get("PacketData", "TID")
    prot = data.get("PacketData", "PROT")

    newPacketData.set("PacketData", "TID", str(tid))
    newPacketData.set("PacketData", "TIME", "0")
    newPacketData.set("PacketData", "activityTimeoutSecs", "240")
    newPacketData.set("PacketData", "PROT", prot)

    Packet(newPacketData).sendPacket(self, "CONN", 0x00000000, 0)
