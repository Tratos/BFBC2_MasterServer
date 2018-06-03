from Utilities.Packet import Packet


def ReceivePacket(self, multiUBRA):
    if multiUBRA:
        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))

        Packet(toSend).send(self, "UBRA", 0x00000000, 0)
        self.CONNOBJ.theaterPacketID += 1

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))

        Packet(toSend).send(self, "UBRA", 0x00000000, 0)
    else:
        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))

        Packet(toSend).send(self, "UBRA", 0x00000000, 0)
