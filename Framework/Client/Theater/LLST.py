from Globals import Servers
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    """ Lobby List """

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    toSend.set("PacketData", "NUM-LOBBIES", "1")  # TODO: Make support for more than one lobby
    Packet(toSend).send(self, "LLST", 0x00000000, 0)

    """ Lobby Data """

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    toSend.set("PacketData", "LID", "1")
    toSend.set("PacketData", "PASSING", str(len(Servers)))
    toSend.set("PacketData", "NAME", "bfbc2_01")
    toSend.set("PacketData", "LOCALE", "en_US")
    toSend.set("PacketData", "MAX-GAMES", "1000")
    toSend.set("PacketData", "FAVORITE-GAMES", "0")
    toSend.set("PacketData", "FAVORITE-PLAYERS", "0")
    toSend.set("PacketData", "NUM-GAMES", str(len(Servers)))
    Packet(toSend).send(self, "LDAT", 0x00000000, 0)
