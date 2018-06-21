from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    lobbyID = str(data.get("PacketData", "LID"))
    gameID = str(data.get("PacketData", "GID"))

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    toSend.set("PacketData", "LID", lobbyID)
    toSend.set("PacketData", "GID", gameID)
    Packet(toSend).send(self, "ECNL", 0x00000000, 0)
