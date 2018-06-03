from Utilities.Packet import Packet


def ReceivePacket(self, data):
    # TODO: Remove player from Joining Players and add player to Active Players

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    toSend.set("PacketData", "PID", str(data.get("PacketData", "PID")))

    Packet(toSend).send(self, "PENT", 0x00000000, 0)
