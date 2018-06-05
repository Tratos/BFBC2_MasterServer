from Utilities.Packet import Packet


def ReceivePacket(self, data):
    self.CONNOBJ.joiningPlayers -= 1
    self.CONNOBJ.activePlayers += 1

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    toSend.set("PacketData", "PID", str(data.get("PacketData", "PID")))

    Packet(toSend).send(self, "PENT", 0x00000000, 0)
