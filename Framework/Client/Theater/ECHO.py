from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet


def ReceiveRequest(self, data, addr):
    newPacketData = ConfigParser()
    newPacketData.optionxform = str
    newPacketData.add_section("PacketData")

    newPacketData.set("PacketData", "TXN", "ECHO")
    newPacketData.set("PacketData", "IP", addr[0])
    newPacketData.set("PacketData", "PORT", str(addr[1]))
    newPacketData.set("PacketData", "ERR", "0")
    newPacketData.set("PacketData", "TYPE", "1")
    newPacketData.set("PacketData", "TID", str(data.get("PacketData", "TID")))

    Packet(newPacketData).sendPacket(self, "ECHO", 0x00000000, 0, addr, logger=Log("TheaterClient", "\033[35;1m"))
