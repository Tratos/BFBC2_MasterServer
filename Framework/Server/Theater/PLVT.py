from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    playerID = str(data.get("PacketData", "PID"))
    lobbyID = str(data.get("PacketData", "LID"))
    gameID = str(data.get("PacketData", "GID"))

    toSend = Packet().create()
    toSend.set("PacketData", "PID", playerID)
    toSend.set("PacketData", "LID", lobbyID)
    toSend.set("PacketData", "GID", gameID)
    Packet(toSend).send(self, "KICK", 0x00000000, 0)

    self.CONNOBJ.activePlayers -= 1
    for player in range(len(self.CONNOBJ.connectedPlayers)):
        if int(playerID) == self.CONNOBJ.connectedPlayers[player].playerID:
            self.CONNOBJ.connectedPlayers[player].playerID = 0
            del self.CONNOBJ.connectedPlayers[player]

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    Packet(toSend).send(self, "PLVT", 0x00000000, 0)
