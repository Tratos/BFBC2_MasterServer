from Utilities.Packet import Packet


def ReceivePacket(self, data):
    self.CONNOBJ.joiningPlayers -= 1
    self.CONNOBJ.activePlayers += 1

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    toSend.set("PacketData", "PID", str(data.get("PacketData", "PID")))

    Packet(toSend).send(self, "PENT", 0x00000000, 0)
