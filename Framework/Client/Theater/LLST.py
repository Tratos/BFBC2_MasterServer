from ConfigParser import ConfigParser

from Globals import Servers
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    """ Lobby List """
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")

    newPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    newPacket.set("PacketData", "NUM-LOBBIES", "1")  # TODO: Make support for more than one lobby
    Packet(newPacket).sendPacket(self, "LLST", 0x00000000, 0)

    """ Lobby Data """
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")

    newPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    newPacket.set("PacketData", "LID", "1")
    newPacket.set("PacketData", "PASSING", str(len(Servers)))
    newPacket.set("PacketData", "NAME", "bfbc2_01")
    newPacket.set("PacketData", "LOCALE", "en_US")
    newPacket.set("PacketData", "MAX-GAMES", "1000")
    newPacket.set("PacketData", "FAVORITE-GAMES", "0")
    newPacket.set("PacketData", "FAVORITE-PLAYERS", "0")
    newPacket.set("PacketData", "NUM-GAMES", str(len(Servers)))
    Packet(newPacket).sendPacket(self, "LDAT", 0x00000000, 0)
